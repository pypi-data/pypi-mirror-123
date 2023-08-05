# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages


setup(
    name="pyftdc",
    version="0.0.9",
    description="A parser for MongoDB FTDC files, with Python bindings.",
    author="Jorge Imperial",
    license="Apache v2",
    packages=find_packages(where = 'src'),
    package_dir={"": "src"},
    cmake_install_dir="src/pyftdc",
    include_package_data = True,
)
