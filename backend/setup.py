# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:22:56 2022

@author: Alexander Pilz
"""
#Imports of required functions
from distutils.core import setup
from Cython.Build import cythonize

#setup for compiling the utils_cy 
#can be executed with python3 setup.py build_ext --inplace
setup(ext_modules = cythonize('utils_cy.pyx', language_level=3))
