#!/usr/bin/python
"""
This example shows the functionality of the PageHeader object.

It creates a sample page with the different types of headers.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, PageStyle, Head, MiniPage
from pylatex.utils import line_break, display_page_number, header1, header2, \
    bold


def generate_header():
    geometry_options = {"margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)
    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")) as left_header:
        left_header.append("Page date: ")
        left_header.append(line_break())
        left_header.append("R3")
    # Create center header
    with header.create(Head("C")) as center_header:
        center_header.append("Company")
    # Create right header
    with header.create(Head("R")) as right_header:
        right_header.append(display_page_number())

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    with doc.create(MiniPage(align='c')) as heading:
        heading.append(header1(bold("Title")))
        heading.append(line_break())
        heading.append(header2(bold("As at:")))

    doc.generate_pdf("header", clean_tex=False)

generate_header()
