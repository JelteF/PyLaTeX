#!/usr/bin/python
"""
This example shows the functionality of the MiniPage element.

It creates a sample page filled with labels using the MiniPage element.

..  :copyright: (c) 2016 by Vladimir Gorovikov and Scott Wallace
    :license: MIT, see License for more details.
"""

# begin-doc-include
from random import randint
from pylatex import Document, LongTabu, HFill, Tabu, LineBreak, Center
from pylatex.utils import bold


def genenerate_tabus():
    geometry_options = {
        "landscape": True,
        "margin": "1.5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True
    }
    doc = Document(page_numbers=True, geometry_options=geometry_options)

    # Generate data table with 'tight' columns
    with doc.create(LongTabu("X[r] X[r] X[r] X[r] X[r] X[r]", spread="0pt")) as data_table:
        header_row1 = ["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"]
        data_table.add_row(header_row1, mapper=[bold])
        data_table.add_hline()
        data_table.add_empty_row()
        data_table.end_table_header()
        data_table.add_row(["Prov", "Num", "CurBal", "IntPay", "Total",
                            "IntR"])
        row = ["PA", "9", "$100", "%10", "$1000", "Test"]
        for i in range(40):
            data_table.add_row(row)

    with doc.create(Center()) as centered:
        with centered.create(Tabu("X[r] X[r]", spread="1in")) as data_table:
            header_row1 = ["X", "Y"]
            data_table.add_row(header_row1, mapper=[bold])
            data_table.add_hline()
            row = [randint(0,1000), randint(0,1000)]
            for i in range(4):
                data_table.add_row(row)

    with doc.create(Center()) as centered:
        with centered.create(Tabu("X[r] X[r]", to="4in")) as data_table:
            header_row1 = ["X", "Y"]
            data_table.add_row(header_row1, mapper=[bold])
            data_table.add_hline()
            row = [randint(0,1000), randint(0,1000)]
            for i in range(4):
                data_table.add_row(row)


    doc.generate_pdf("tabus", clean_tex=False)

genenerate_tabus()
