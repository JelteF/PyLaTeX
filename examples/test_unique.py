import os

from pylatex import Document, PageStyle, Head, Foot, Tabular, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongColoredTable, LongTabu, \
    ColoredTabularx
from pylatex.utils import header1, header2, bold, NoEscape, line_break, \
    text_color, display_page_number, new_line, page_break


def generate_unique():
    geometry_options = {
        "headheight": "75pt",
        "margin": "0.5in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    # Generating first page style
    first_page = PageStyle("firstpage")

    # Header image
    header_left = Head("L")
    logo_wrapper = MiniPage(width=NoEscape(r"0.49\textwidth"), adjustment='c')
    logo_file = os.path.join(os.path.dirname(__file__), 'sample-logo.png')
    logo = StandAloneGraphic(image_options="width=120px", filename=logo_file)
    logo_wrapper.append(logo)
    header_left.append(logo_wrapper)

    header_center = Head("C")

    # Add document title
    header_right = Head("R")
    title_wrapper = MiniPage(width=NoEscape(r"0.49\textwidth"), adjustment='c',
                             align='r')
    title_wrapper.append(bold(header1("Bank Account Statement")))
    title_wrapper.append(line_break())
    title_wrapper.append(bold(header2("Date")))
    header_right.append(title_wrapper)

    # Add footer
    footer_center = Foot("C")
    message = "Important message please read"
    footer_table = ColoredTabularx("X X X X",
                                   arguments=NoEscape(r"\textwidth"))
    footer_table.add_row(
        [MultiColumn(4, align='l', data=text_color(message, "blue"))])
    footer_table.add_hline(color="blue")
    footer_table.add_empty_row()

    branch_address = MiniPage(
        width=NoEscape(r"0.25\textwidth"),
        adjustment='t')
    branch_address.append("960 - 22nd street east")
    branch_address.append(line_break())
    branch_address.append("Saskatoon, SK")

    document_details = MiniPage(width=NoEscape(r"0.25\textwidth"),
                                adjustment='t', align='r')
    document_details.append("1000")
    document_details.append(line_break())
    document_details.append(display_page_number())

    footer_table.add_row([branch_address, branch_address, branch_address,
                          document_details])

    footer_center.append(footer_table)

    first_page.append(header_left)
    first_page.append(header_center)
    first_page.append(header_right)
    first_page.append(footer_center)

    doc.preamble.append(first_page)
    # End first page style

    # Start other page style
    other_style = PageStyle("otherstyle")

    # Add logo to left header
    header_left = Head("L")
    header_table = Tabular(NoEscape("m{2.5in}|m{2.1in}|m{2.5in}"))
    logo_wrapper = MiniPage(width=NoEscape(r"0.33\textwidth"), adjustment='t!',
                            align='l')
    logo_wrapper.append(StandAloneGraphic(image_options="width=150px",
                                          filename=logo_file))

    # Add recipent information
    header_center = Head("C")
    customer = MiniPage(width=NoEscape(r"0.33\textwidth"), adjustment='h',
                        align='l')
    customer.append("Some Person")
    customer.append(line_break())
    customer.append("For some Person")
    customer.append(line_break())
    customer.append("Address1")
    customer.append(line_break())
    customer.append("Address2")
    customer.append(line_break())
    customer.append("Address3")

    # Add branch information
    header_right = Head("R")
    statement_details = MiniPage(width=NoEscape(r"0.33\textwidth"),
                                 adjustment='h', align='r')
    statement_details.append(bold("Bank Account Statement"))
    statement_details.append(line_break())
    statement_details.append("Date")
    statement_details.append(line_break())
    statement_details.append("Branch no. - Account no.")
    statement_details.append(line_break())
    statement_details.append("1181 - Asdasd")
    statement_details.append(line_break())
    statement_details.append("TlB Chequing")

    header_table.add_row([logo_wrapper, customer, statement_details])
    header_center.append(header_table)
    other_style.append(header_left)
    other_style.append(header_center)
    other_style.append(header_right)
    other_style.append(footer_center)

    doc.preamble.append(other_style)
    # End Page Styles

    # Add customer information
    first_page_table = Tabu("X[l] X[r]")

    customer = MiniPage(width=NoEscape(r"0.49\textwidth"), adjustment='h')
    customer.append("Verna Volcano")
    customer.append(new_line())
    customer.append("For some Person")
    customer.append(new_line())
    customer.append("Address1")
    customer.append(new_line())
    customer.append("Address2")
    customer.append(new_line())
    customer.append("Address3")

    # Add branch information
    branch = MiniPage(width=NoEscape(r"0.49\textwidth"), adjustment='t!',
                      align='r')
    branch.append("Branch no.")
    branch.append(line_break())
    branch.append(bold("1181..."))
    branch.append(line_break())
    branch.append(bold("TIB Cheque"))

    first_page_table.add_row([customer, branch])
    first_page_table.add_empty_row()

    # Add advisor information
    advisor = MiniPage(width=NoEscape(r"\textwidth"), adjustment='h')
    advisor.append("Info about advisor")
    advisor.append(new_line())
    advisor.append("Stuff and things")
    advisor_row = MultiColumn(2, data=advisor)

    first_page_table.add_row([advisor_row])

    doc.append(first_page_table)

    doc.change_document_style("otherstyle")

    doc.change_page_style("firstpage")

    doc.add_color(name="lightgray", model="gray", description="0.80")

    # Add statement table
    data_table = LongColoredTable("X[l] X[2l] X[r] X[r] X[r]", row_height=1.5)
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

    doc.append(data_table)

    doc.append(page_break())

    # Add cheque images
    cheque_table = LongTabu("X[c] X[c]")
    cheque_file = os.path.join(os.path.dirname(__file__), 'chequeexample.png')
    cheque = StandAloneGraphic(cheque_file, image_options="width=200px")
    for i in range(0, 20):
        cheque_table.add_row([cheque, cheque])
    doc.append(cheque_table)

    doc.generate_pdf("test_unique", clean_tex=False)

generate_unique()
