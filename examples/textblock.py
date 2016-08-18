#!/usr/bin/python
"""
This example shows the functionality of the TextBlock element.

It creates a sample cheque to demonstrate the positioning of the elements on
the page.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, MiniPage, TextBlock
from pylatex.utils import huge, bold, header2, small1, horizontal_skip, \
    vertical_skip

geometry_options = {"margin": "0.5in"}
doc = Document(indent=False, geometry_options=geometry_options)
doc.change_length("\TPHorizModule", "1mm")
doc.change_length("\TPVertModule", "1mm")

with doc.create(MiniPage(width=r"\textwidth")) as page:
    with page.create(TextBlock(100, 0, 0)) as text_amount_wrapper:
        text_amount_wrapper.append("**** Ten Thousand Dollars")

    with page.create(TextBlock(100, 0, 30)) as address_wrapper:
        address_wrapper.append("COMPANY NAME")
        address_wrapper.append("\nSTREET, ADDRESS")
        address_wrapper.append("\nCITY, POSTAL CODE")

    with page.create(TextBlock(100, 150, 40)) as void_wrapper:
        void_wrapper.append(huge(bold("VOID")))

    with page.create(TextBlock(80, 150, 0)) as date_wrapper:
        date_wrapper.append("DATE")
        date_wrapper.append(header2(bold("2016 06 07\n")))
        date_wrapper.append(horizontal_skip("10mm"))
        date_wrapper.append(small1("Y/A M/M D/J"))

    with page.create(TextBlock(70, 150, 30)) as amount_wrapper:
        amount_wrapper.append(header2(bold("$***** 10,000.00")))

    page.append(vertical_skip("100mm"))

doc.generate_pdf("textblock", clean_tex=False)
