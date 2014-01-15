"""
PyLatex
-------

PyLatex is a Python library for creating LaTeX files. The point of this library
is being able to be an easy, but extensible interface between Python and Latex.


"""
from distutils.core import setup
setup(name='PyLatex',
      version='0.1.0',
      author='Jelte Fennema',
      author_email='pylatex@jeltef.nl',
      description='A Python library for creating LaTeX files',
      long_description=__doc__,
      packages=['pylatex'],
      url='https://github.com/JelteF/PyLatex',
      license='MIT',
      )
