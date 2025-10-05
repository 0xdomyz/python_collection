from Cython.Build import cythonize
from setuptools import setup

setup(
    name="new app",
    ext_modules=cythonize("integrate_cy.pyx"),
    zip_safe=False,
)

setup(
    name="new app 2",
    ext_modules=cythonize("integrate_cy_naive.pyx"),
    zip_safe=False,
)

setup(
    name="new app 3",
    ext_modules=cythonize("integrate_cy_cdef.pyx"),
    zip_safe=False,
)
