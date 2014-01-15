"""
PyLatex
-------

PyLatex is a Python library for creating LaTeX files. The point of this library
is being an easy, but extensible interface between Python and Latex.


Features
~~~~~~~~

The library contains some basic features I have had the need for so far.
Currently those are:

- Document generation and compilation
- Section, table and package classes
- An escape function
- Bold and italic functions

Everything else you want you can still add to the document by adding LaTeX
formatted strings.
"""
from distutils.core import setup
setup(name='PyLatex',
      version='0.2.0',
      author='Jelte Fennema',
      author_email='pylatex@jeltef.nl',
      description='A Python library for creating LaTeX files',
      long_description=__doc__,
      packages=['pylatex'],
      url='https://github.com/JelteF/PyLatex',
      license='MIT',
      )
