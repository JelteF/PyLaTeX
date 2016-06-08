import os
import csv

from pylatex import *
from pylatex.utils import *

def generate_unique():
    doc = Document(header_height='70pt')
   
    # Generating first page style 
    first_page = PageStyle("firstpage")
  
    # Header image
    header_left = Head("L")
    logo_wrapper = Minipage(width=NoEscape(r"0.49\textwidth"), adjustment='h')
    logo_file = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')
    logo = StandAloneGraphic(width="120px", filename=logo_file)
    logo_wrapper.append(logo)
    header_left.append(logo_wrapper)

    header_center = Head("C")

    # Add document title
    header_right = Head("R")
    title_wrapper = Minipage(width=NoEscape(r"0.49\textwidth"), adjustment='h')
    title_right = Flushright()
    title_right.append(bold(header1("Bank Account Statement")))
    title_right.append(NoEscape(line_break()))
    title_right.append(bold(header2("Date")))
    title_wrapper.append(title_right)
    header_right.append(title_wrapper)

    # Add footer
    footer_center = Foot("C")
    message = "Important message please read"
    footer_table = Tabular(NoEscape("m{1.5in} m{1.5in} m{2in} m{2in}"))
    footer_table.add_row([MultiColumn(4, align='r', data=text_color(message, "blue"))])
    footer_table.add_hline(color="blue")
    footer_table.add_empty_row()

    branch_address = Minipage(width=NoEscape(r"0.25\textwidth"), adjustment='h')
    branch_address.append("960 - 22nd street east")
    branch_address.append("\nSaskatoon, SK")

    document_details = Minipage(width=NoEscape(r"0.25\textwidth"),
            adjustment='h')
    document_details_right = Flushright()
    document_details_right.append("1000")
    document_details_right.append(line_break())
    document_details_right.append(display_page_number())
    document_details.append(document_details_right)

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
    logo_wrapper = Minipage(width=NoEscape(r"0.33\textwidth"), adjustment='t!')
    logo_wrapper_left = Flushleft()
    logo_wrapper_left.append(StandAloneGraphic(width="150px", filename=logo_file))
    logo_wrapper.append(logo_wrapper_left)
    header_left.append(logo_wrapper)

    # Add recipent information
    header_center = Head("C")
    customer = Minipage(width=NoEscape(r"0.33\textwidth"), adjustment='h')
    customer_left = Flushleft()
    customer_left.append("Verna Volcano")
    customer_left.append(line_break())
    customer_left.append("For some Person")
    customer_left.append(line_break())
    customer_left.append("Address1")
    customer_left.append(line_break())
    customer_left.append("Address2")
    customer_left.append(line_break())
    customer_left.append("Address3")
    customer.append(customer_left)
    header_center.append(customer)

    # Add branch information
    header_right = Head("R")
    statement_details = Minipage(width=NoEscape(r"0.33\textwidth"),
        adjustment='h')
    statement_right = Flushright()
    statement_right.append(bold("Bank Account Statement"))
    statement_right.append(line_break())
    statement_right.append("Date")
    statement_right.append(line_break())
    statement_right.append("Branch no. - Account no.")
    statement_right.append(line_break())
    statement_right.append("1181 - Asdasd")
    statement_right.append(line_break())
    statement_right.append("TlB Chequing")
    statement_details.append(statement_right)
    header_right.append(statement_details)

    other_style.append(header_left)
    other_style.append(header_center)
    other_style.append(header_right)
    other_style.append(footer_center)

    doc.preamble.append(other_style)
    # End Page Styles

    # Add customer information
    first_page_table = Tabu("X[l] X[r]")

    customer = Minipage(width=NoEscape(r"0.49\textwidth"), adjustment='h')
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
    branch = Minipage(width=NoEscape(r"0.49\textwidth"), adjustment='t!')
    branch_right = Flushright()
    branch_right.append("Branch no.")
    branch_right.append(line_break())
    branch_right.append(bold("1181..."))
    branch_right.append(line_break())
    branch_right.append(bold("TIB Cheque"))
    branch.append(branch_right)

    first_page_table.add_row([customer, branch])

    # Add advisor information
    advisor = Minipage(width=NoEscape(r"\textwidth"), adjustment='h')
    advisor.append("Info about advisor")
    advisor.append(new_line())
    advisor.append("Stuff and things")
    advisor_row = MultiColumn(2, data=advisor)

    first_page_table.add_row([ advisor_row ])

    doc.append(first_page_table)
    
    doc.change_document_style("otherstyle")

    doc.change_page_style("firstpage")

    doc.add_color(name="lightgray", model="gray", description="0.80")

    # Add statement table
    data_table = LongColoredTable("X[l] X[2l] X[r] X[r] X[r]", row_height=1.5)
    data_table.add_row(["date", "description", "debits($)", "credits($)", "balance($)"], mapper=bold, color="lightgray")
    data_table.add_empty_row()
    data_table.add_hline()
    path_to_data = os.path.join(os.path.dirname(__file__), 'data.csv')
    with open(path_to_data, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in csv_reader:
            if i == 1:
                data_table.add_row(row, color="lightgray")
                i = 0
            else:
                data_table.add_row(row)
                i = 1

    doc.append(data_table)

    doc.append(page_break())
    
    # Add cheque images
    cheque_table = LongTabu("X[c] X[c]")
    cheque_file = os.path.join(os.path.dirname(__file__), 'chequeexample.png')
    cheque = StandAloneGraphic(cheque_file, width="200px")
    for i in range(0,20):
        cheque_table.add_row([cheque, cheque])
    doc.append(cheque_table)

    doc.generate_tex("Example_Unique")

generate_unique()
