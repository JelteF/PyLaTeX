#!/usr/bin/python
"""
This example shows the functionality of the MiniPage element.

It creates a sample page filled with labels using the MiniPage element.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, LongTabu, HFill
from pylatex.utils import bold, center


def genenerate_longtabu():
    geometry_options = {
        "landscape": True,
        "margin": "0.5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True
    }
    doc = Document(page_numbers=True, geometry_options=geometry_options)

    # Generate data table
    with doc.create(LongTabu("X[r] X[r] X[r] X[r] X[r] X[r]")) as data_table:
        header_row1 = ["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"]
        data_table.add_row(header_row1, mapper=[bold, center])
        data_table.add_hline()
        data_table.add_empty_row()
        data_table.end_table_header()
        data_table.add_row(["Prov", "Num", "CurBal", "IntPay", "Total",
                            "IntR"])
        row = ["PA", "9", "$100", "%10", "$1000", "Test"]
        for i in range(50):
            data_table.add_row(row)

    doc.append(bold("Grand Total:"))
    doc.append(HFill())
    doc.append(bold("Total"))

    doc.generate_pdf("longtabu", clean_tex=False)

genenerate_longtabu()
