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
    MultiRow, Command, Matrix, VectorName, Quantity, TableRowSizeError, \
    LongTable, ColoredTable, Position, FlushLeft, FlushRight, Center, \
    MiniPage, TextBlock, PageStyle, Head, Foot, StandAloneGraphic
from pylatex.utils import escape_latex, fix_filename, dumps_list, bold, \
    italic, verbatim, center, flush_left, flush_right, huge, header1, \
    header2, small1, small2, text_color, page_break, new_line, line_break, \
    horizontal_fill, vertical_skip, horizontal_skip, display_page_number, \
    text_box

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
        lscape=True,
        margin="0.5in",
        page_numbers=True,
        header_height="12pt",
        indent=False
    )

    repr(doc)

    doc.append('Some text.')
    doc.change_page_style(style="empty")
    doc.change_document_style(style="plain")
    doc.add_color(name="lightgray", model="gray", description="0.6")
    doc.add_color(name="abitless", model="gray", description="0.8")
    doc.change_length(parameter=r"\headheight", value="0.5in")

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

    t.add_row(cells=(1, 2), escape=False, strict=True, mapper=[bold, center])

    # MultiColumn/MultiRow.
    t.add_row((MultiColumn(size=2, align='|c|', data='MultiColumn'),),
              strict=True)

    # One multiRow-cell in that table would not be proper LaTeX,
    # so strict is set to False
    t.add_row((MultiRow(size=2, width='*', data='MultiRow'),), strict=False)

    repr(t)

    # Long Table
    longtable = LongTable(table_spec='c c c')
    longtable.add_row(["test", "test2", "test3"])
    longtable.end_table_header()

    # Colored Table
    coloredtable = ColoredTable(table_spec='X[c] X[c]')
    coloredtable.add_row(["test", "test2"], color="gray", mapper=bold)


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

    # StandAloneGraphic
    stand_alone_graphic = StandAloneGraphic(filename='',
                                            width=r"0.8\textwidth")
    repr(stand_alone_graphic)


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

    enum = Enumerate(enumeration_symbol="a)")
    enum.add_item(s="item")
    enum.add_item(s="item2")
    enum.append("append")
    repr(enum)

    desc = Description()
    desc.add_item(label="label", s="item")
    desc.append("append")
    repr(desc)


def test_headfoot():
    # Page styles, headers and footers
    page_style = PageStyle("NewStyle")
    page_style.change_thickness("header", "1pt")
    page_style.change_thickness("footer", "1pt")

    header = Head("C")
    header.append("append")

    footer = Foot("C")
    footer.append("append")

    page_style.append(header)
    page_style.append(footer)
    repr(header)
    repr(footer)
    repr(page_style)


def test_position():
    # Test alignment environments
    position = Position()
    repr(position)

    center = Center()
    center.append("append")
    repr(center)

    right = FlushRight()
    right.append("append")
    repr(right)

    left = FlushLeft()
    left.append("append")
    repr(left)

    minipage = MiniPage(width=r"\textwidth", height="10pt", adjustment='t',
                        align='r')
    minipage.append("append")
    repr(minipage)

    textblock = TextBlock(width="200", horizontal_pos="200",
                          vertical_pos="200", indent=True)
    textblock.append("append")
    textblock.dumps()
    repr(textblock)


def test_utils():
    # Utils
    escape_latex(s='')

    fix_filename(path='')

    dumps_list(l=[], escape=False, token='\n')

    bold(s='')

    italic(s='')

    verbatim(s='', delimiter='|')

    text_color(s='green text', color='green')

    page_break()

    line_break()

    new_line()

    horizontal_fill()

    horizontal_skip(size='20pt')

    display_page_number()

    huge(s='HugeText')

    header1(s='Header1Text')

    header2(s='Header2Text')

    small1(s='Small1Text')

    small2(s='Small2Text')

    vertical_skip(size="20pt")

    text_box(s="TextBoxText")

    center(s="CenteredText")

    flush_left(s="FlushedLeft")

    flush_right(s="FlushedRight")


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
