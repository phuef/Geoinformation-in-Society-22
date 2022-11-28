# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:22:56 2022

@author: Alexander Pilz
"""
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('utils_cy.pyx', language_level=3))