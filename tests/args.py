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
matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot

from pylatex import Document, Section, Math, Tabular, Figure, SubFigure, \
    Package, TikZ, Axis, Plot, Itemize, Enumerate, Description, MultiColumn, \
    MultiRow, Command, Matrix, VectorName, Quantity
from pylatex.utils import escape_latex, fix_filename, dumps_list, bold, \
    italic, verbatim


def test_document():
    doc = Document(
        default_filepath='default_filepath',
        documentclass='article',
        fontenc='T1',
        inputenc='utf8',
        data=None,
    )

    doc.append('Some text.')

    doc.generate_tex(filepath='')
    doc.generate_pdf(filepath='', clean=True)


def test_section():
    Section(title='', numbering=True, data=None)


def test_math():
    Math(data=None, inline=False)

    VectorName(name='')

    # Numpy
    m = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])

    Matrix(matrix=m, mtype='p', alignment=None)


def test_table():
    # Tabular
    t = Tabular(table_spec='|c|c|', data=None, pos=None)

    t.add_hline(start=None, end=None)

    t.add_row(cells=(1, 2), escape=False)

    # MultiColumn/MultiRow.
    t.add_row((MultiColumn(size=2, align='|c|', data='MultiColumn'),))

    t.add_row((MultiRow(size=2, width='*', data='MultiRow'),))


def test_command():
    Command(command='documentclass', arguments=None, options=None,
            packages=None)


def test_graphics():
    f = Figure(data=None, position=None)

    f.add_image(filename='', width=r'0.8\textwidth', placement=r'\centering')

    f.add_caption(caption='')

    # Subfigure
    s = SubFigure(data=None, position=None,
                  width=r'0.45\linewidth', separate_paragraph=False)

    s.add_image(filename='', width='r\linewidth',
                placement=None)

    s.add_caption(caption='')

    # Matplotlib
    plot = Figure(data=None, position=None)

    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    pyplot.plot(x, y)

    plot.add_plot(width=r'0.8\textwidth', placement=r'\centering')
    plot.add_caption(caption='I am a caption.')


def test_quantities():
    # Quantities
    Quantity(quantity=1*pq.kg)
    Quantity(quantity=1*pq.kg, format_cb=lambda x: str(int(x)))


def test_package():
    # Package
    Package(name='', options=None)


def test_tikz():
    # PGFPlots
    TikZ(data=None)

    Axis(data=None, options=None)

    Plot(name=None, func=None, coordinates=None, error_bar=None, options=None)


def test_lists():
    # Lists
    itemize = Itemize()
    itemize.add_item(s="item")
    itemize.append("append")

    enum = Enumerate()
    enum.add_item(s="item")
    enum.append("append")

    desc = Description()
    desc.add_item(label="label", s="item")
    desc.append("append")


def test_utils():
    # Utils
    escape_latex(s='')

    fix_filename(path='')

    dumps_list(l=[], escape=False, token='\n')

    bold(s='')

    italic(s='')

    verbatim(s='', delimiter='|')
