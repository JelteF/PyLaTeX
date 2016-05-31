from pylatex import *
from pylatex.utils import page_break, horizontal_fill, page_number, text_box

test_doc = Document(lscape=True)

test_doc.add_header(lhead="Left head", chead="center head", rhead=page_number())

#test_header = Header(lhead="Test", rhead="Test right", chead="Test left")

#print(test_header.dumps())

#test_doc.append(test_header)

#print (test_doc.dumps())

test_table = Tabu("X[c]|X[c]|X[c]")

test_table.add_row(['aasdasasdasdkjnasjkcnasdk ajshndjkasnajksndasjkdnsakjnajsdnksajndkansdjksna','b','c'])

center_text = Center()

right_text = Flushright()

right_text.append("This is right alligned")

center_text.append("This is centered")

test_doc.append(test_table)

test_doc.append(page_break())

test_doc.append(text_box("This is a test"))

test_doc.append("right")

test_doc.append(horizontal_fill())

test_doc.append("left")


test_doc.append(center_text)

test_doc.append(right_text)

test_doc.generate_tex("test")

print("Done")

