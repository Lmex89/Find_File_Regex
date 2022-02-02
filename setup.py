#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Test',
    ext_modules=cythonize("find_py.py"),
    zip_safe=False,
)
