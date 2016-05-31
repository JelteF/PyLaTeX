from pylatex import *
from pylatex.utils import *
import csv
import os.path

def gen_r3_rsp():
    doc = Document(lscape=True, page_numbers=True, margin='0.5in')
    doc.add_header(lhead="Print Date: R3",
        chead="Pacific & Western Bank", rhead=page_number())

    heading = Center()
    heading.append(header1(bold("RSP Savings Trial Balance")))
    doc.append(heading)
    subheading = Center()
    subheading.append(header2(bold("As at:")))
    doc.append(subheading)
    
    data_table = LongTabu("X[r] X[r] X[r] X[r] X[r] X[r]")
    header_row1 = [["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"]]
    data_table.add_table_header(header_row1, mapper=[bold,center])
    data_table.add_empty_row()
    data_table.add_row(["Prov", "Num", "CurBal", "IntPay", "Total", "IntR"])
    with open('test.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            data_table.add_row(row)

    doc.append(data_table)

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


