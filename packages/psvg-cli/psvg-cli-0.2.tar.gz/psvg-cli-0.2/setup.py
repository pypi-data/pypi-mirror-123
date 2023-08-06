import os

from setuptools import setup

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="psvg-cli",
    description="Apply transformations to Parametric SVG files",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="James Scott-Brown",
    author_email="james@jamesscottbrown.com",
    url="https://github.com/jamesscottbrown/psvg-cli",
    project_urls={
        "Source": "https://github.com/jamesscottbrown/psvg-cli",
        "Issues": "https://github.com/jamesscottbrown/psvg-cli/issues",
    },
    classifiers=[],
    keywords="",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["psvg_cli"],
    entry_points="""
        [console_scripts]
        psvg-cli=psvg_cli.cli:cli
    """,
    install_requires=[
        "cairosvg==2.5.2",
        "click==8.0.0a1",
        "sympy==1.7.1",
        "tabulate==0.8.9"
    ],
    extras_require={"test": ["pytest"]},
    tests_require=["psvg_cli[test]"],
)
