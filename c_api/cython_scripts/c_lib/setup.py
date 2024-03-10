from Cython.Build import cythonize
from setuptools import setup

setup(
    name="new app",
    ext_modules=cythonize("atoi.pyx"),
    zip_safe=False,
)
