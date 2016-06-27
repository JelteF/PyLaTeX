#!/usr/bin/python

from pylatex import Document, LongTabu, MiniPage
from pylatex.utils import line_break


def generate_labels():
    doc = Document()

    doc.change_document_style("empty")

    table_of_labels = LongTabu("X[l] X[l]")
    label = MiniPage(width=r"0.5\textwidth")
    label.append("Vladimir Gorovikov")
    label.append(line_break())
    label.append("Company Name")
    label.append(line_break())
    label.append("Somewhere, City")
    label.append(line_break())
    label.append("Country")

    for i in range(0, 20):
        table_of_labels.add_row(([label, label]))
        table_of_labels.add_empty_row()

    doc.append(table_of_labels)

    doc.generate_pdf("test_labels", clean_tex=False)


generate_labels()
