#!/usr/bin/python
"""
This example shows the functionality of the MiniPage element.

It creates a sample page filled with labels using the MiniPage element.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, LineBreak, MiniPage, VerticalSpace


def generate_labels():
    geometry_options = {"margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)

    doc.change_document_style("empty")

    for i in range(10):
        with doc.create(MiniPage(width=r"0.5\textwidth")):
            doc.append("Vladimir Gorovikov")
            doc.append("\n")
            doc.append("Company Name")
            doc.append("\n")
            doc.append("Somewhere, City")
            doc.append("\n")
            doc.append("Country")

        if (i % 2) == 1:
            doc.append(VerticalSpace("20pt"))
            doc.append(LineBreak())

    doc.generate_pdf("minipage", clean_tex=False)


generate_labels()
