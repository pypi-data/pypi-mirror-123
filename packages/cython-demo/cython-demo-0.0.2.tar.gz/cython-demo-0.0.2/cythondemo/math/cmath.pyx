# distutils:language=c++
# cython:language_level=3

import cython
from libc.math cimport sqrt

@cython.binding(True)
cpdef double heron(double a, double b, double c):
    """
    This is the documentation of heron_c.
    """
    cdef double p;
    p = (a + b + c) / 2.0
    return sqrt(p * (p - a) * (p - b) * (p - c))
