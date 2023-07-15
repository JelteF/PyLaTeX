#!/usr/bin/python
"""
This example shows the functionality of the PyLaTeX library.

It creates a sample report with 2 tables, one containing images and the other
containing data. It also creates a complex header with an image.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
import os

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number
from pylatex.utils import bold, NoEscape


def generate_unique():
    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    # Generating first page style
    first_page = PageStyle("firstpage")

    # Header image
    with first_page.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c')) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__),
                                     'sample-logo.png')
            logo_wrapper.append(StandAloneGraphic(image_options="width=120px",
                                filename=logo_file))

    # Add document title
    with first_page.create(Head("R")) as right_header:
        with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                 pos='c', align='r')) as title_wrapper:
            title_wrapper.append(LargeText(bold("Bank Account Statement")))
            title_wrapper.append(LineBreak())
            title_wrapper.append(MediumText(bold("Date")))

    # Add footer
    with first_page.create(Foot("C")) as footer:
        message = "Important message please read"
        with footer.create(Tabularx(
                "X X X X",
                width_argument=NoEscape(r"\textwidth"))) as footer_table:

            footer_table.add_row(
                [MultiColumn(4, align='l', data=TextColor("blue", message))])
            footer_table.add_hline(color="blue")
            footer_table.add_empty_row()

            branch_address = MiniPage(
                width=NoEscape(r"0.25\textwidth"),
                pos='t')
            branch_address.append("960 - 22nd street east")
            branch_address.append("\n")
            branch_address.append("Saskatoon, SK")

            document_details = MiniPage(width=NoEscape(r"0.25\textwidth"),
                                        pos='t', align='r')
            document_details.append("1000")
            document_details.append(LineBreak())
            document_details.append(simple_page_number())

            footer_table.add_row([branch_address, branch_address,
                                  branch_address, document_details])

    doc.preamble.append(first_page)
    # End first page style

    # Add customer information
    with doc.create(Tabu("X[l] X[r]")) as first_page_table:
        customer = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='h')
        customer.append("Verna Volcano")
        customer.append("\n")
        customer.append("For some Person")
        customer.append("\n")
        customer.append("Address1")
        customer.append("\n")
        customer.append("Address2")
        customer.append("\n")
        customer.append("Address3")

        # Add branch information
        branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
                          align='r')
        branch.append("Branch no.")
        branch.append(LineBreak())
        branch.append(bold("1181..."))
        branch.append(LineBreak())
        branch.append(bold("TIB Cheque"))

        first_page_table.add_row([customer, branch])
        first_page_table.add_empty_row()

    doc.change_document_style("firstpage")
    doc.add_color(name="lightgray", model="gray", description="0.80")

    # Add statement table
    with doc.create(LongTabu("X[l] X[2l] X[r] X[r] X[r]",
                             row_height=1.5)) as data_table:
        data_table.add_row(["date",
                            "description",
                            "debits($)",
                            "credits($)",
                            "balance($)"],
                           mapper=bold,
                           color="lightgray")
        data_table.add_empty_row()
        data_table.add_hline()
        row = ["2016-JUN-01", "Test", "$100", "$1000", "-$900"]
        for i in range(30):
            if (i % 2) == 0:
                data_table.add_row(row, color="lightgray")
            else:
                data_table.add_row(row)

    doc.append(NewPage())

    # Add cheque images
    with doc.create(LongTabu("X[c] X[c]")) as cheque_table:
        cheque_file = os.path.join(os.path.dirname(__file__),
                                   'chequeexample.png')
        cheque = StandAloneGraphic(cheque_file, image_options="width=200px")
        for i in range(0, 20):
            cheque_table.add_row([cheque, cheque])

    doc.generate_pdf("complex_report", clean_tex=False)

generate_unique()
