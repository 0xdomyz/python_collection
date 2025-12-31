from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension(
        name="logparse",
        sources=["logparse.pyx"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="cython-logparse",
    ext_modules=cythonize(extensions, language_level=3),
)
