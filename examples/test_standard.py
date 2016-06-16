from pylatex import *
from pylatex.utils import *
import csv
import os.path

def gen_r3_rsp():
    doc = Document(lscape=True, page_numbers=True, margin='0.5in')

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
    with open('test.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data_table.add_row(row)

    doc.append(data_table)

    doc.append(bold("Grand Total:") + horizontal_fill() + bold("Total"))

    doc.generate_pdf("Example_Standard")

def generate_csv():
    with open('test.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        
        for i in range(0,5000):
            csv_writer.writerow(['Test1','Test2','Test3','Test4','Test5',
                'Test6'])

if not os.path.isfile('test.csv'):
    generate_csv()

gen_r3_rsp()


