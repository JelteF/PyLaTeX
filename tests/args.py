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
    LongTable, FlushLeft, FlushRight, Center, MiniPage, TextBlock, \
    PageStyle, Head, Foot, StandAloneGraphic, Tabularx, Column, NewLine, \
    LineBreak, NewPage, HFill, HugeText, LargeText, MediumText, \
    SmallText, FootnoteText, TextColor, FBox, MdFramed, Tabu, \
    HorizontalSpace, VerticalSpace
from pylatex.utils import escape_latex, fix_filename, dumps_list, bold, \
    italic, verbatim, NoEscape

matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot  # noqa


def test_document():
    geometry_options = {
        "includeheadfoot": True,
        "headheight": "12pt",
        "headsep": "10pt",
        "landscape": True
    }

    doc = Document(
        default_filepath='default_filepath',
        documentclass='article',
        fontenc='T1',
        inputenc='utf8',
        lmodern=True,
        data=None,
        page_numbers=True,
        indent=False,
        document_options=["a4paper", "12pt"],
        geometry_options=geometry_options
    )

    repr(doc)

    doc.append('Some text.')
    doc.change_page_style(style="empty")
    doc.change_document_style(style="plain")
    doc.add_color(name="lightgray", model="gray", description="0.6")
    doc.add_color(name="abitless", model="gray", description="0.8")
    doc.set_variable(name="myVar", value="1234")
    doc.set_variable(name="myVar", value="1234")
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
    t = Tabular(table_spec='|c|c|', data=None, pos=None, width=2)

    t.add_hline(start=None, end=None)

    t.add_row(cells=(1, 2), escape=False, strict=True, mapper=[bold])

    # MultiColumn/MultiRow.
    t.add_row((MultiColumn(size=2, align='|c|', data='MultiColumn'),),
              strict=True)

    # One multiRow-cell in that table would not be proper LaTeX,
    # so strict is set to False
    t.add_row((MultiRow(size=2, width='*', data='MultiRow'),), strict=False)

    repr(t)

    # TabularX
    tabularx = Tabularx(table_spec='X X X', arguments=NoEscape(r"\textwidth"))
    tabularx.add_row(["test1", "test2", "test3"])

    # Long Table
    longtable = LongTable(table_spec='c c c')
    longtable.add_row(["test", "test2", "test3"])
    longtable.end_table_header()

    # Colored Tabu
    coloredtable = Tabu(table_spec='X[c] X[c]')
    coloredtable.add_row(["test", "test2"], color="gray", mapper=bold)

    # Colored Tabularx
    coloredtable = Tabularx(table_spec='X[c] X[c]')
    coloredtable.add_row(["test", "test2"], color="gray", mapper=bold)

    # Column
    column = Column("R", "X", r"\raggedleft", parameters=2)
    repr(column)


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
    stand_alone_graphic = StandAloneGraphic(
        filename='', image_options=r"width=0.8\textwidth")
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

    enum = Enumerate(enumeration_symbol=r"\alph*)", options={'start': 172})
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

    repr(HorizontalSpace(size='20pt', star=False))

    repr(VerticalSpace(size="20pt", star=True))

    # Test alignment environments
    center = Center()
    center.append("append")
    repr(center)

    right = FlushRight()
    right.append("append")
    repr(right)

    left = FlushLeft()
    left.append("append")
    repr(left)

    minipage = MiniPage(width=r"\textwidth", height="10pt", pos='t',
                        align='r', content_pos='t', fontsize="Large")
    minipage.append("append")
    repr(minipage)

    textblock = TextBlock(width="200", horizontal_pos="200",
                          vertical_pos="200", indent=True)
    textblock.append("append")
    textblock.dumps()
    repr(textblock)


def test_frames():
    # Tests the framed environments

    md_framed = MdFramed()
    md_framed.append("Framed text")
    repr(md_framed)

    f_box = FBox()
    f_box.append("Fboxed text")
    repr(f_box)


def test_basic():
    # Tests the basic commands and environments
    # Basic commands
    new_page = NewPage()
    repr(new_page)

    new_line = NewLine()
    repr(new_line)

    line_break = LineBreak()
    repr(line_break)

    h_fill = HFill()
    repr(h_fill)

    # Basic environments
    huge = HugeText("Huge")
    huge.append("Huge 2")
    repr(huge)

    large = LargeText("Large")
    large.append("Large 2")
    repr(large)

    medium = MediumText("Medium")
    medium.append("Medium 2")
    repr(medium)

    small = SmallText("Small")
    small.append("Small 2")
    repr(small)

    footnote = FootnoteText("Footnote")
    footnote.append("Footnote 2")
    repr(footnote)

    text_color = TextColor("green", "GreenText")
    text_color.append("More Green Text")
    repr(text_color)


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
