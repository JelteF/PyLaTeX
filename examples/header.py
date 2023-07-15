#!/usr/bin/python
"""
This example shows the functionality of the PageHeader object.

It creates a sample page with the different types of headers and footers.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import (
    Document,
    Foot,
    Head,
    LargeText,
    LineBreak,
    MediumText,
    MiniPage,
    PageStyle,
    simple_page_number,
)
from pylatex.utils import bold


def generate_header():
    geometry_options = {"margin": "0.7in"}
    doc = Document(geometry_options=geometry_options)
    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append("Page date: ")
        header.append(LineBreak())
        header.append("R3")
    # Create center header
    with header.create(Head("C")):
        header.append("Company")
    # Create right header
    with header.create(Head("R")):
        header.append(simple_page_number())
    # Create left footer
    with header.create(Foot("L")):
        header.append("Left Footer")
    # Create center footer
    with header.create(Foot("C")):
        header.append("Center Footer")
    # Create right footer
    with header.create(Foot("R")):
        header.append("Right Footer")

    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    with doc.create(MiniPage(align="c")):
        doc.append(LargeText(bold("Title")))
        doc.append(LineBreak())
        doc.append(MediumText(bold("As at:")))

    doc.generate_pdf("header", clean_tex=False)


generate_header()
