#!/usr/bin/python

from pylatex import Document, PageStyle, Head, Foot, MiniPage, LongTabu
from pylatex.utils import line_break, display_page_number, header1, header2, \
    bold, horizontal_fill, center
import csv
import os.path


def gen_r3_rsp():
    doc = Document(lscape=True, page_numbers=True, margin='0.5in',
                   header_height="20pt", header_sep="10pt")

    # Add document header
    header = PageStyle("header")
    left_header = Head("L")
    left_header.append("Page date: ")
    left_header.append(line_break())
    left_header.append("R3")
    center_header = Head("C")
    center_header.append("Company")
    right_header = Head("R")
    right_header.append(display_page_number())
    center_footer = Foot("C")
    header.append(left_header)
    header.append(center_header)
    header.append(right_header)
    header.append(center_footer)
    doc.preamble.append(header)
    doc.change_document_style("header")

    # Add Heading
    heading = MiniPage(align='c')
    heading.append(header1(bold("Title")))
    heading.append(line_break())
    heading.append(header2(bold("As at:")))
    doc.append(heading)

    # Generate data table
    data_table = LongTabu("X[r] X[r] X[r] X[r] X[r] X[r]")
    header_row1 = ["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"]
    data_table.add_row(header_row1, mapper=[bold, center])
    data_table.add_hline()
    data_table.add_empty_row()
    data_table.end_table_header()
    data_table.add_row(["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"])
    row = ["PA", "9", "$100", "%10", "$1000", "Test"]
    for i in range(50):
        data_table.add_row(row)

    doc.append(data_table)

    doc.append(bold("Grand Total:"))
    doc.append(horizontal_fill())
    doc.append(bold("Total"))

    doc.generate_pdf("test_standard")

gen_r3_rsp()
