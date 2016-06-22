#!/usr/bin/python

from pylatex import Document, MiniPage, TextBlock, MultiColumn, Tabu
from pylatex.utils import huge, bold, header2, small1, horizontal_skip, \
    horizontal_fill, vertical_skip, page_break

doc = Document(page_numbers=False)
doc.change_length("\TPHorizModule", "1mm")
doc.change_length("\TPVertModule", "1mm")
doc.change_length("\parindent", "0pt")

page = MiniPage(width=r"\textwidth")

text_amount_wrapper = TextBlock(100, 0, 0)

text_amount_wrapper.append("**** Ten Thousand Dollars")

address_wrapper = TextBlock(100, 0, 30)

address_wrapper.append("COMPANY NAME")
address_wrapper.append("\nSTREET, ADDRESS")
address_wrapper.append("\nCITY, POSTAL CODE")

void_wrapper = TextBlock(100, 150, 40)
void_wrapper.append(huge(bold("VOID")))

date_wrapper = TextBlock(80, 150, 0)

date_wrapper.append("DATE")
date_wrapper.append(header2(bold("2016 06 07\n")))
date_wrapper.append(horizontal_skip("10mm"))
date_wrapper.append(small1("Y/A M/M D/J"))

amount_wrapper = TextBlock(70, 150, 30)

amount_wrapper.append(header2(bold("$***** 10,000.00")))

page.append(address_wrapper)
page.append(date_wrapper)
page.append(amount_wrapper)
page.append(text_amount_wrapper)
page.append(void_wrapper)

page.append(vertical_skip("100mm"))

cheque_info = Tabu("X[l] X[l]")

heading = MultiColumn(2, align='l', data=bold("TFSA TRANSFER"))

cheque_info.add_row([heading])
cheque_info.add_empty_row()

details_wrapper = MiniPage(width=r"0.4\textwidth")
details_wrapper.append("Cheque number")
details_wrapper.append(horizontal_fill())
details_wrapper.append(bold("testNo"))

details2_wrapper = MiniPage(width=r"0.4\textwidth")
details2_wrapper.append("Cheque date")
details2_wrapper.append(horizontal_fill())
details2_wrapper.append(bold("testDate"))

cheque_info.add_row([details_wrapper, details2_wrapper])

page.append(cheque_info)


doc.append(page)
doc.append(page_break())
doc.append(page)

doc.generate_pdf("test_cheque")
