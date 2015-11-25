#!/usr/bin/python

"""
Test to check when arguments of functions get changed.

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""

import numpy as np
import quantities as pq
import matplotlib

from pylatex import Document, Section, Math, Tabular, Figure, SubFigure, \
    Package, TikZ, Axis, Plot, Itemize, Enumerate, Description, MultiColumn, \
    MultiRow, Command, Matrix, VectorName, Quantity, TableRowSizeError
from pylatex.utils import escape_latex, fix_filename, dumps_list, bold, \
    italic, verbatim

matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot  # noqa


def test_document():
    doc = Document(
        default_filepath='default_filepath',
        documentclass='article',
        fontenc='T1',
        inputenc='utf8',
        lmodern=True,
        data=None,
    )

    repr(doc)

    doc.append('Some text.')

    doc.generate_tex(filepath='')
    doc.generate_pdf(filepath='', clean=True)


def test_section():
    sec = Section(title='', numbering=True, data=None)
    repr(sec)


def test_math():
    math = Math(data=None, inline=False)
    repr(math)

    vec = VectorName(name='')
    repr(vec)

    # Numpy
    m = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])

    matrix = Matrix(matrix=m, mtype='p', alignment=None)
    repr(matrix)


def test_table():
    # Tabular
    t = Tabular(table_spec='|c|c|', data=None, pos=None)

    t.add_hline(start=None, end=None)

    t.add_row(cells=(1, 2), escape=False, strict=True)

    # MultiColumn/MultiRow.
    t.add_row((MultiColumn(size=2, align='|c|', data='MultiColumn'),),
              strict=True)

    # One multiRow-cell in that table would not be proper LaTeX,
    # so strict is set to False
    t.add_row((MultiRow(size=2, width='*', data='MultiRow'),), strict=False)

    repr(t)


def test_command():
    c = Command(command='documentclass', arguments=None, options=None,
                packages=None)
    repr(c)


def test_graphics():
    f = Figure(data=None, position=None)

    f.add_image(filename='', width=r'0.8\textwidth', placement=r'\centering')

    f.add_caption(caption='')
    repr(f)

    # Subfigure
    s = SubFigure(data=None, position=None, width=r'0.45\linewidth')

    s.add_image(filename='', width='r\linewidth',
                placement=None)

    s.add_caption(caption='')
    repr(s)

    # Matplotlib
    plot = Figure(data=None, position=None)

    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    pyplot.plot(x, y)

    plot.add_plot(width=r'0.8\textwidth', placement=r'\centering')
    plot.add_caption(caption='I am a caption.')
    repr(plot)


def test_quantities():
    # Quantities
    Quantity(quantity=1*pq.kg)
    q = Quantity(quantity=1*pq.kg, format_cb=lambda x: str(int(x)))
    repr(q)


def test_package():
    # Package
    p = Package(name='', options=None)
    repr(p)


def test_tikz():
    # PGFPlots
    t = TikZ(data=None)
    repr(t)

    a = Axis(data=None, options=None)
    repr(a)

    p = Plot(name=None, func=None, coordinates=None, error_bar=None,
             options=None)
    repr(p)


def test_lists():
    # Lists
    itemize = Itemize()
    itemize.add_item(s="item")
    itemize.append("append")
    repr(itemize)

    enum = Enumerate()
    enum.add_item(s="item")
    enum.append("append")
    repr(enum)

    desc = Description()
    desc.add_item(label="label", s="item")
    desc.append("append")
    repr(desc)


def test_utils():
    # Utils
    escape_latex(s='')

    fix_filename(path='')

    dumps_list(l=[], escape=False, token='\n')

    bold(s='')

    italic(s='')

    verbatim(s='', delimiter='|')


def test_errors():
    # Errors

    # TableRowSizeError

    # General test

    try:
        raise TableRowSizeError
    except TableRowSizeError:
        pass

    # Positive test, expected to raise Error

    t = Tabular(table_spec='|c|c|', data=None, pos=None)
    try:
        # Wrong number of cells in table should raise an exception
        t.add_row(cells=(1, 2, 3), escape=False, strict=True)
    except TableRowSizeError:
        pass

    # Negative test, should not raise
    try:
        # Wrong number with strict=False should not raise an exception
        t.add_row(cells=(1, 2, 3), escape=False, strict=False)
    except TableRowSizeError:
        raise
