import click
from tabulate import tabulate

import os
from psvg_cli import utils
from functools import update_wrapper


@click.group()
@click.version_option()
def cli():
    """Apply transformations to Parametric SVG files"""


@cli.group(chain=True, help='Modify a parametric SVG file or files')
@click.version_option()
def process():
    pass


@process.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass


@cli.command()
@click.argument("input_files", type=click.File("rb"), nargs=-1, required=True)
@click.option('-c', '--csv', help='Format output as CSV, rather than pretty-printed table')
@click.option('--full-name/--short-name', help='Show full file path as provided as argument, or just file name',
              required=False, default=False)
def parameters(input_files, csv, full_name):
    """List parameters and their default values"""

    fieldnames, rows = utils.tabulate_params(input_files, full_name)

    if csv:
        print(",".join(fieldnames))
        for row in rows:
            vals = [row.get(k, "") for k in fieldnames]
            print(",".join(vals))
    else:
        table = []
        for row in rows:
            vals = [row.get(k, "") for k in fieldnames]
            table.append(vals)

        print(tabulate(table, headers=fieldnames))


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """

    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """

    @processor
    def new_func(stream, *args, **kwargs):
        yield from stream
        yield from f(*args, **kwargs)

    return update_wrapper(new_func, f)


###################

@process.command("open")
@click.option(
    "-i",
    "--image",
    "images",
    type=click.Path(),
    multiple=True,
    help="The image file to open.",
)
# @click.argument("images", type=click.Path(), nargs=-1, required=True)
# N.B.: if this is an argument, the next command gets recongised as an input ile, throwing error
@generator
def open_cmd(images):
    """Loads one or multiple images for processing.  The input parameter
    can be specified multiple times to load more than one image.
    """
    for image_path in images:
        try:
            click.echo(f"Opening '{image_path}'")
            img = utils.open_image(image_path)
            yield (img, image_path)
        except Exception as e:
            click.echo(f"Could not open image '{image_path}': {e}", err=True)

@process.command("opendir")
@click.argument("dir", type=click.Path(), nargs=1, required=True)
@generator
def open_cmd(dir):
    """Loads all images in a directory for processing.
    """
    for file_name in os.listdir(dir):
        image_path = os.path.join(dir, file_name)
        if not file_name.endswith(".svg"):
            click.echo(f"Skipping file {file_name} as it does not have .svg extension")
            continue

        try:
            click.echo(f"Opening '{image_path}'")
            img = utils.open_image(image_path)
            yield (img, image_path)
        except Exception as e:
            click.echo(f"Could not open image '{image_path}': {e}", err=True)


@process.command("remove_parametric_params")
@processor
def remove_parametric_params_cmd(images):
    """
    Removes the parametric attributes, leaving the non-parametric ones in place.
    """
    for (image_data, filename) in images:
        yield (utils.remove_parametric_attributes(image_data), filename)


# TODO: rename to something like update_nonparametric_attribute or apply_parametric_attributes?
@process.command("convert_parametric_attributes")
@processor
def convert_parametric_attributes_cmd(images):
    """
    Updates values of non-parametric attributes based on parametric equivalents.
    """
    for (image_data, filename) in images:
        yield (utils.remove_parametric_attributes(image_data), filename)


@process.command("delete_by_class")
@click.option(
    "-c",
    "--class",
    "classes",
    multiple=True,
    required=True,
    help="The class(es) to be deleted.",
)
@processor
def delete_by_class(images, classes):
    """
    Delete elements with a particular class.
    """
    for (image_data, filename) in images:
        for class_name in classes:
            image_data = utils.remove_by_class(image_data, class_name)
        yield (image_data, filename)


@process.command("apply_transformation")
@click.option(
    "-t",
    "--transformation",
    "transformation",
    default="transform({width}, {height})",
    help="transformation to apply.",
)
@processor
def apply_transformation_cmd(images, transformation):
    """
    Apply transformation.
    """
    for (image_data, filename) in images:
        image_data = utils.apply_transformation(image_data, transformation)
        yield (image_data, filename)


@process.command("style_class")
@click.option(
    "-c",
    "--class",
    "class_name",
    required=True,
    help="Class to style.",
)
@click.option(
    "-s",
    "--style",
    "style",
    required=True,
    help="Style to apply.",
)
@processor
def style_class(images, class_name, style):
    """
    Apply style to a class - replacing existing style.
    """
    for (image_data, filename) in images:
        image_data = utils.apply_style(image_data, class_name, style)
        yield (image_data, filename)


@process.command("substitute_params")
@click.option(
    "-o",
    "--old",
    "old",
    required=True,
    help="Old expression to be replaced.",
)
@click.option(
    "-n",
    "--new",
    "new",
    required=True,
    help="New expression to replace old expression.",
)
@processor
def substitute_params(images, old, new):
    """
    Preform substitution in parametric expression.
    """
    for (image_data, filename) in images:
        image_data = utils.substitute(image_data, old, new)
        yield (image_data, filename)


@process.command("delete_unused_parameters")
@processor
def delete_unused_parameters(images):
    """
    Delete assignment of default values to any parameters that are not used in any parametric expressions.
    """
    for (image_data, filename) in images:
        image_data = utils.delete_unused_parameters(image_data)
        yield (image_data, filename)


@process.command("save")
@processor
@click.option(
    "--dir",
    default="processed",
    type=click.Path(),
    help="The output directory.",
    show_default=True,
)
@click.option('--format', type=click.Choice(['svg', 'png', 'pdf', 'all'], case_sensitive=False))
def save_cmd(images, dir, format):
    """Saves all processed images to a series of files."""

    if not os.path.exists(dir):
        click.echo(f"Creating directory {dir}")
        os.makedirs(dir)

    for image_data, image_filename in images:
        try:
            utils.save_image(image_data, image_filename, dir, format)
            yield
        except Exception as e:
            click.echo(f"Could not save image '{image_filename}'", err=True)
            print(e)
