"""
PyLaTeX
-------

PyLaTeX is a Python library for creating LaTeX files. The goal of this library
is being an easy, but extensible interface between Python and LaTeX.


Features
~~~~~~~~

The library contains some basic features I have had the need for so far.
Currently those are:

- Document generation and compilation
- Section, table, math and package classes
- A matrix class that can compile NumPy ndarrays and matrices to LaTeX
- An escape function
- Bold and italic functions
- Every class has a dump method, which writes the output to a filepointer

Everything else you want you can still add to the document by adding LaTeX
formatted strings instead of classes or regular strings.


Dependencies
~~~~~~~~~~~~

- Python 3.3 (Python 3.x might work as well)
- pdflatex (only if you want to compile the tex file)
- NumPy (only if you want to convert it's matrixes)
- ordered-set


Installation
~~~~~~~~~~~~

::

    pip install pylatex


Example
~~~~~~~

.. code:: python

    import numpy as np

    from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
        Plot
    from pylatex.numpy import Matrix
    from pylatex.utils import italic

    doc = Document()
    section = Section('Yaay the first section, it can even be ' + italic('italic'))

    section.append('Some regular text')

    math = Subsection('Math that is incorrect', data=[Math(data=['2*3', '=', 9])])

    section.append(math)
    table = Table('rc|cl')
    table.add_hline()
    table.add_row((1, 2, 3, 4))
    table.add_hline(1, 2)
    table.add_empty_row()
    table.add_row((4, 5, 6, 7))

    table = Subsection('Table of something', data=[table])

    section.append(table)

    a = np.array([[100, 10, 20]]).T
    M = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])

    math = Math(data=[Matrix(M), Matrix(a), '=', Matrix(M*a)])
    equation = Subsection('Matrix equation', data=[math])

    section.append(equation)

    tikz = TikZ()

    axis = Axis(options='height=6cm, width=6cm, grid=major')

    plot1 = Plot(name='model', func='-x^5 - 242')
    coordinates = [
        (-4.77778, 2027.60977),
        (-3.55556, 347.84069),
        (-2.33333, 22.58953),
        (-1.11111, -493.50066),
        (0.11111, 46.66082),
        (1.33333, -205.56286),
        (2.55556, -341.40638),
        (3.77778, -1169.24780),
        (5.00000, -3269.56775),
    ]

    plot2 = Plot(name='estimate', coordinates=coordinates)

    axis.append(plot1)
    axis.append(plot2)

    tikz.append(axis)

    plot_section = Subsection('Random graph', data=[tikz])

    section.append(plot_section)

    doc.append(section)

    doc.generate_pdf()

This code will generate this:

.. image:: https://raw.github.com/JelteF/PyLaTeX/master/docs/static/screenshot.png


Future development
~~~~~~~~~~~~~~~~~~

I will keep adding functionality I need to this library, an interface for
graphics and math will probably be added in a future version.

If you add a feature yourself, or fix a bug, please send a pull request.

You can submit issues, but it will not be my priority to fix them. My job and
education are a bit higher on the priority list.


Support
~~~~~~~

This library is being developed for Python 3.3. It currently doesn't work for
Python 2.7, but it's mostly syntax and import changes that break it for 2.7.
It is also only tested on Linux, so it might not work on any different
platforms.

I have no intention of testing on any different platforms or with different
Python versions. I also don't have the intention to write fixes for platform or
environment specific bugs, but pull requests that fix those are always welcome.

Copyright and License
~~~~~~~~~~~~~~~~~~~~~

Copyright 2014 Jelte Fennema, under `the MIT license
<https://github.com/JelteF/PyLaTeX/blob/master/LICENSE>`_.

"""


try:
    from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name='PyLaTeX',
      version='0.4.2',
      author='Jelte Fennema',
      author_email='pylatex@jeltef.nl',
      description='A Python library for creating LaTeX files',
      long_description=__doc__,
      packages=['pylatex'],
      url='https://github.com/JelteF/PyLaTeX',
      license='MIT',
      install_requires=['ordered-set'],
      )
