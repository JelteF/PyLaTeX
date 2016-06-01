from pylatex import *
from pylatex.utils import *
import csv
import os.path

def gen_r3_rsp():
    doc = Document(lscape=True, page_numbers=True, margin='0.5in')
    doc.add_header(lhead="Print Date: R3",
        chead="Pacific & Western Bank", rhead=page_number())


    minipageleft = Minipage(width=0.4)
    address2 = Flushleft()
    address2.append("Left text")
    minipageleft.append(address2)
    doc.append(minipageleft)
    doc.append(horizontal_fill())
    minipageright = Minipage(width=0.4)
    address1 = Flushright()
    address1.append("Text")
    minipageright.append(address1)
    doc.append(minipageright)

    heading = Center()
    heading.append(header1(bold("RSP Savings Trial Balance")))
    doc.append(heading)
    subheading = Center()
    subheading.append(header2(bold("As at:")))
    doc.append(subheading)
    
    data_table = LongTabu("X[r] X[r] X[r] X[r] X[r] X[r]")
    header_row1 = ["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"]
    data_table.add_row(header_row1)
    data_table.add_hline()
    data_table.add_empty_row()
    data_table.end_table_header()
    data_table.add_row(["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"])
    with open('test.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            data_table.add_row(row)

    doc.append(data_table)
    
    doc.append(bold("Grand Total:") + horizontal_fill() + bold("Total"))

    doc.generate_tex("Example_R3")

def generate_csv():
    with open('test.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        
        for i in range(0,5000):
            csv_writer.writerow(['Test1','Test2','Test3','Test4','Test5',
                'Test6'])

if not os.path.isfile('test.csv'):
    generate_csv()

gen_r3_rsp()
print("Done")


