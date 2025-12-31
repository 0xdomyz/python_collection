from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension(
        name="diffusion",
        sources=["diffusion.pyx"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="cython-diffusion",
    ext_modules=cythonize(extensions, language_level=3),
)
