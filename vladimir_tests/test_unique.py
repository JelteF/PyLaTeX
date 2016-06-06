import os
import csv

from pylatex import *
from pylatex.utils import *

def generate_unique():
    doc = Document(header_height='60pt')
    doc.change_page_style('empty')
    
    header = Header()
    logo_file = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')

    logo_wrapper = Minipage(width=0.33, adjustment='h')
    logo_wrapper.append(StandAloneGraphic(width="150px", filename=logo_file))

    customer = Minipage(width=0.33, adjustment='h')
    customer_left = Flushleft()
    customer_left.append("Verna Volcano")
    customer_left.append(NoEscape(line_break()))
    customer_left.append("For some Person")
    customer_left.append(NoEscape(line_break()))
    customer_left.append("Address1")
    customer_left.append(NoEscape(line_break()))
    customer_left.append("Address2")
    customer_left.append(NoEscape(line_break()))
    customer_left.append("Address3")
    customer.append(customer_left)

    statement_details = Minipage(width=0.33, adjustment='h')
    statement_right = Flushright()
    statement_right.append(bold("Bank Account Statement"))
    statement_right.append(NoEscape(line_break()))
    statement_right.append("Date")
    statement_right.append(NoEscape(line_break()))
    statement_right.append("Branch no. - Account no.")
    statement_right.append(NoEscape(line_break()))
    statement_right.append("1181 - Asdasd")
    statement_right.append(NoEscape(line_break()))
    statement_right.append("TlB Chequing")
    statement_details.append(statement_right)

    header.set_params("lhead", logo_wrapper)
    header.set_params("chead", customer)
    header.set_params("rhead", statement_details)

    footer = Footer(header_exists=True)

    footer.set_params("lfoot", "this is a test footer")

    doc.append(header)
    doc.append(footer)

    doc.remove_header_and_footer()

    # Add versabank logo
    first_page = Tabu("X[c] X[r]")
    logo_wrapper = Minipage(width=0.49, adjustment='h')
    image_file = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')
    logo = StandAloneGraphic(width="120px", filename=image_file)
    logo_wrapper.append(logo)
    # doc.append(logo_wrapper)

    # doc.append(horizontal_fill())

    # Add document title
    title_wrapper = Minipage(width=0.49, adjustment='h')
    title_right = Flushright()
    title_right.append(bold(header1("Bank Account Statement")))
    title_right.append(NoEscape(line_break()))
    title_right.append(bold(header2("Date")))
    title_wrapper.append(title_right)
    #doc.append(title_wrapper)

    first_page.add_row([logo_wrapper, title_wrapper])

    # Add customer information
    customer = Minipage(width=0.49, adjustment='h')
    customer.append("Verna Volcano")
    customer.append("For some Person")
    customer.append("Address1")
    customer.append("Address2")
    customer.append("Address3")
    #doc.append(customer)

    # Add branch information
    branch = Minipage(width=0.49, adjustment='h')
    branch_right = Flushright()
    branch_right.append("Branch no.")
    branch_right.append(bold("1181..."))
    branch_right.append(bold("TIB Cheque"))
    branch.append(branch_right)
    #doc.append(branch)

    first_page.add_row([customer, branch])

    #doc.append(NoEscape(line_break()))

    # Add advisor information
    advisor = Minipage(width=1, adjustment='h')
    advisor.append("Info about advisor")
    advisor.append("Stuff and things")
    #doc.append(advisor)

    advisor_row = MultiColumn(2, data=advisor)

    first_page.add_row([advisor, ''])
    
    doc.append(first_page)
    
    doc.add_color(name="lightgray", model="gray", description="0.80")

    # Add statement table
    data_table = LongColoredTable("X[l] X[2l] X[r] X[r] X[r]")
    data_table.add_row(["date", "description", "debits($)", "credits($)", "balance($)"], mapper=bold, color="lightgray")
    data_table.add_empty_row()
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
    cheque = StandAloneGraphic("200px", cheque_file)
    for i in range(0,20):
        cheque_table.add_row([cheque, cheque])
    doc.append(cheque_table)


    

    doc.generate_tex("Example_Unique")

generate_unique()
