#!/usr/bin/python
"""
This example shows the functionality of the MiniPage element.

It creates a sample page filled with labels using the MiniPage element.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, LongTabu, MiniPage


def generate_labels():
    geometry_options = {"margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)

    doc.change_document_style("empty")

    with doc.create(LongTabu("X[l] X[l]")) as table_of_labels:
        label = MiniPage(width=r"0.5\textwidth")
        label.append("Vladimir Gorovikov")
        label.append("\n")
        label.append("Company Name")
        label.append("\n")
        label.append("Somewhere, City")
        label.append("\n")
        label.append("Country")

        for i in range(0, 20):
            table_of_labels.add_row(([label, label]))
            table_of_labels.add_empty_row()

    doc.generate_pdf("minipage", clean_tex=False)


generate_labels()
