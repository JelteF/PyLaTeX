import os
import csv

from pylatex import *
from pylatex.utils import *

def generate_unique():
    doc = Document()
    doc.change_page_style('empty')
    
    header = Header(header_height=20, footer_height=20)
    logo_file = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')
    header.set_lhead(StandAloneGraphic("200px", logo_file).dumps())

    doc.append(header)

    # Add versabank logo
    logo_wrapper = Minipage(width=0.49)
    image_file = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')
    logo = StandAloneGraphic(width="120px", filename=image_file)
    logo_wrapper.append(logo)
    doc.append(logo_wrapper)

    doc.append(horizontal_fill())

    # Add document title
    title_wrapper = Minipage(width=0.49)
    title_right = Flushright()
    title_right.append(bold(header1("Bank Account Statement")))
    title_right.append(bold(header2("\nDate")))
    title_wrapper.append(title_right)
    doc.append(title_wrapper)

    # Add customer information
    customer = Minipage(width=0.49, adjustment='t')
    customer.append("Verna Volcano")
    customer.append("\nFor some Person")
    customer.append("\nAddress1")
    customer.append("\nAddress2")
    customer.append("\nAddress3")
    doc.append(customer)

    # Add branch information
    branch = Minipage(width=0.49, adjustment='t')
    branch_right = Flushright()
    branch_right.append("Branch no.")
    branch_right.append(bold("\n1181..."))
    branch_right.append(bold("\nTIB Cheque"))
    branch.append(branch_right)
    doc.append(branch)

    doc.append(line_break())

    # Add advisor information
    advisor = Minipage(width=1, adjustment='t')
    advisor.append("Info about advisor")
    advisor.append("\nStuff and things")
    doc.append(advisor)

    doc.add_skip("1in")
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
