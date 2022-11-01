"""python3.9 setup.py build_ext --inplace"""

from Cython.Build import cythonize
from setuptools import setup

setup(
    name="new app",
    ext_modules=cythonize("example1.pyx"),
    zip_safe=False,
)

setup(
    name="new app",
    ext_modules=cythonize("example2.pyx"),
    zip_safe=False,
)
