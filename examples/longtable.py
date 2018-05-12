#!/usr/bin/python
"""
This example shows the functionality of the longtable element.

It creates a sample multi-page spanning table

..  :copyright: (c) 2017 by Jarrah Gosbell
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, LongTable, MultiColumn


def genenerate_longtabu():
    geometry_options = {
        "margin": "2.54cm",
        "includeheadfoot": True
    }
    doc = Document(page_numbers=True, geometry_options=geometry_options)

    # Generate data table
    with doc.create(LongTable("l l l")) as data_table:
            data_table.add_hline()
            data_table.add_row(["header 1", "header 2", "header 3"])
            data_table.add_hline()
            data_table.end_table_header()
            data_table.add_hline()
            data_table.add_row((MultiColumn(3, align='r',
                                data='Continued on Next Page'),))
            data_table.add_hline()
            data_table.end_table_footer()
            data_table.add_hline()
            data_table.add_row((MultiColumn(3, align='r',
                                data='Not Continued on Next Page'),))
            data_table.add_hline()
            data_table.end_table_last_footer()
            row = ["Content1", "9", "Longer String"]
            for i in range(150):
                data_table.add_row(row)

    doc.generate_pdf("longtable", clean_tex=False)

genenerate_longtabu()
