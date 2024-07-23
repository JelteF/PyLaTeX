#!/usr/bin/python
"""
This example shows the functionality of the TextBlock element.

It creates a sample cheque to demonstrate the positioning of the elements on
the page.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import (
    Document,
    HorizontalSpace,
    HugeText,
    MediumText,
    MiniPage,
    SmallText,
    TextBlock,
    VerticalSpace,
)
from pylatex.utils import bold

geometry_options = {"margin": "0.5in"}
doc = Document(indent=False, geometry_options=geometry_options)
doc.change_length("\TPHorizModule", "1mm")
doc.change_length("\TPVertModule", "1mm")

with doc.create(MiniPage(width=r"\textwidth")) as page:
    with page.create(TextBlock(100, 0, 0)):
        page.append("**** Ten Thousand Dollars")

    with page.create(TextBlock(100, 0, 30)):
        page.append("COMPANY NAME")
        page.append("\nSTREET, ADDRESS")
        page.append("\nCITY, POSTAL CODE")

    with page.create(TextBlock(100, 150, 40)):
        page.append(HugeText(bold("VOID")))

    with page.create(TextBlock(80, 150, 0)):
        page.append("DATE")
        page.append(MediumText(bold("2016 06 07\n")))
        page.append(HorizontalSpace("10mm"))
        page.append(SmallText("Y/A M/M D/J"))

    with page.create(TextBlock(70, 150, 30)):
        page.append(MediumText(bold("$***** 10,000.00")))

    page.append(VerticalSpace("100mm"))

doc.generate_pdf("textblock", clean_tex=False)
