"""Instalador para el paquete "pyoperaciones"."""

from setuptools import setup

long_description = (
    open('README.txt').read()
    + '\n' +
    open('LICENSE').read()
    + '\n')

setup(
    name="pyprimos_Caleb",
    version="1.0",
    description="A tool to perform mathematical operations.",
    long_description=long_description,
    classifiers=[
        # Indica la estabilidad del proyecto. Los valores comunes son
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indique a quien va dirigido su proyecto
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        # Indique licencia usada (debe coincidir con el "license")
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Indique versiones soportas, Python 2, Python 3 o ambos.
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="pyprimos_Caleb mathematical operations",
    author="Caleb Villanueva",
    author_email="calebzamalloa90@gmail.com",
    license="GNU GPLv3",
    packages=["pyprimos_Caleb"]
)
