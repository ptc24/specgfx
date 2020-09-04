import setuptools
from setuptools import setup
from Cython.Build import cythonize
#from distutils.core import setup


setup(name="specgfx",
    version="0.0.1dev1",
    description="ZX spectrum inspired text and graphics",
    author="Peter Corbett",
    author_email="peter.corbett@cantab.net",
    url="https://github.com/ptc24/specgfx/",
    packages=["specgfx"],
    ext_modules = cythonize("specgfx/cyrender.pyx"),
    install_requires=[
        "numpy",
        "pygame",
        "cython"
    ]
    )