#!/usr/bin/python3

from pylatex import Document, Section, Table
from pylatex.utils import italic

doc = Document()
section = Section('Yaaaay the first section, it can even be ' +
                  italic('italic'))

table = Table('r|cl')
table.add_hline()
table.add_row((1, 2, 3))
table.add_hline(1, 2)
table.add_empty_row()
table.add_row((4, 5, 6))

section.content.append(table)
doc.content.append(section)
doc.generate_pdf()
