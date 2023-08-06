import os
import re
import xml.etree.ElementTree as ET

import sympy
from cairosvg import svg2png, svg2pdf

base_dir = '../glyph_definitions'


def tabulate_params(input_files, full_name=True):
    all_params = set(['glyphtype', 'soterms'])

    rows = []

    for file in input_files:

        (base_name, extension) = os.path.splitext(file.name)

        if not full_name:
            base_name = base_name.split('/')[-1]

        # if extension != ".svg":
        #    continue

        tree = ET.parse(file)
        svg_tree = tree.getroot()

        param_string = svg_tree.attrib['{https://parametric-svg.github.io/v0.2}defaults']

        assignments = param_string.split(';')

        row = {'name': base_name}
        for assignment in assignments:
            (var_name, value) = assignment.split('=')
            row[var_name] = value
            all_params.add(var_name)

        row['glyphtype'] = svg_tree.attrib['glyphtype']
        row['soterms'] = svg_tree.attrib['soterms']

        rows.append(row)

    fieldnames = ['name']
    fieldnames.extend(all_params)

    return fieldnames, rows


#####################################

def open_image(file):
    tree = ET.parse(file)
    svg_tree = tree.getroot()
    return svg_tree


def remove_parametric_attributes(root):
    # This function simply removes the parametric attributes, leaving the non-parametric ones in place

    root.attrib.pop('{https://parametric-svg.github.io/v0.2}defaults')

    for child in root:
        parametric_attributes = []
        for attrib in child.attrib:
            if attrib.startswith('{https://parametric-svg.github.io/v0.2}'):
                parametric_attributes.append(attrib)

        for attrib in parametric_attributes:
            child.attrib.pop(attrib)

    return root


def convert_parametric_attributes(root):
    # This function updates the non-parametric attributes, by substituting the default values into the parametric attributes

    default_value_string = root.attrib['{https://parametric-svg.github.io/v0.2}defaults']
    default_values = {}
    for term in default_value_string.split(";"):
        key, value = term.split("=")
        default_values[key] = value

    prefix = '{https://parametric-svg.github.io/v0.2}'

    def evaluate_function(matchobj):
        expr_string = matchobj.group(1)

        expr = sympy.sympify(expr_string)
        for var in default_values:
            expr = expr.subs(var, default_values[var])
        return str(float(expr))

    for child in root:
        parametric_attributes = []
        for attrib in child.attrib:
            if attrib.startswith(prefix):
                parametric_attributes.append(attrib)

        for attrib in parametric_attributes:
            parametric_expression = child.attrib[attrib]
            non_parametric_attribute_name = attrib.replace(prefix, '')
            child.attrib[non_parametric_attribute_name] = re.sub(r'\{(.*?)\}', evaluate_function, parametric_expression)

    return root


def delete_unused_parameters(svg_tree):
    used_parametric_attributes = set()

    def get_parameter_names(expr_string):
        params = set()
        for match in re.finditer(r'\{(.*?)\}', expr_string):
            params = params.union(sympy.sympify(match.group(1)).free_symbols)
        return params

    for child in svg_tree:
        for attrib in child.attrib:
            if attrib.startswith('{https://parametric-svg.github.io/v0.2}'):
                symbols = get_parameter_names(child.attrib[attrib])
                used_parametric_attributes = used_parametric_attributes.union(symbols)

    used_parametric_attributes = [str(x) for x in used_parametric_attributes]

    param_string = svg_tree.attrib['{https://parametric-svg.github.io/v0.2}defaults']
    assignments = param_string.split(';')
    filtered_assignments = []
    for assignment in assignments:
        (var_name, value) = assignment.split('=')
        if var_name in used_parametric_attributes:
            filtered_assignments.append(assignment)

    svg_tree.attrib['{https://parametric-svg.github.io/v0.2}defaults'] = ";".join(filtered_assignments)

    return svg_tree


def remove_by_class(parent_node, class_name):
    nodes_to_remove = []
    for child in parent_node:
        if child.attrib['class'] == class_name:
            nodes_to_remove.append(child)

    for child_node in nodes_to_remove:
        parent_node.remove(child_node)
    return parent_node


def apply_transformation(root, transform):
    g = ET.Element('g')

    g.attrib["transform"] = transform

    while len(root) > 0:
        for child in root:
            print("\tMoving child:", child)
            g.append(child)
            root.remove(child)

    for child in root:
        print("WUT?")

    root.append(g)
    return root


def apply_style(image_data, class_name, style):
    for child in image_data:
        if child.attrib.get('class') == class_name:
            child.attrib['style'] = style
    return image_data


def substitute(svg_tree, old, new):
    def convert_attribute_value(expr_string):
        return re.sub(r'\{(.*?)\}', convert_expression, expr_string)

    def convert_expression(matchobj):
        expr_string = matchobj.group(1)
        expr = sympy.sympify(expr_string).subs(old, new)
        return '{%s}' % str(expr)

    for child in svg_tree:
        for attrib in child.attrib:
            if attrib.startswith('{https://parametric-svg.github.io/v0.2}'):
                child.attrib[attrib] = convert_attribute_value(child.attrib[attrib])

    return svg_tree


####################################################

def save_image(image_data, image_filename, dirname, format):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("parametric", "https://parametric-svg.github.io/v0.2")

    svg_string = ET.tostring(image_data, encoding="unicode")
    output_filename = os.path.join(dirname, image_filename.split('/')[-1])

    if not format or format == 'svg':
        with open(output_filename, 'w') as f:
            f.write(svg_string)
    elif format == 'png':
        svg2png(bytestring=svg_string, write_to=output_filename.replace('.svg', '.png'))
    elif format == 'pdf':
        svg2pdf(bytestring=svg_string, write_to=output_filename.replace('.svg', '.pdf'))
    elif format == 'all':
        save_image(image_data, image_filename, dirname, 'svg')
        save_image(image_data, image_filename, dirname, 'png')
        save_image(image_data, image_filename, dirname, 'pdf')

################################################
