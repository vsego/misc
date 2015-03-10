#!/usr/bin/env python3

"""
A simple program that prints the version of Python and
some of its commonly used libraries (SciPy, NumPy, Matplotlib).
"""

import platform
print("Python version:    ", platform.python_version())

print("NumPy version:      ", end="")
try:
    import numpy
    print(numpy.__version__) 
except ImportError:
    print("not installed")

print("SciPy version:      ", end="") 
try:
    import scipy
    print(scipy.__version__) 
except ImportError:
    print("not installed")

print("Matplotlib version: ", end="") 
try:
    import matplotlib
    print(matplotlib.__version__) 
except ImportError:
    print("not installed")
