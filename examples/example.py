#!/usr/bin/python3

from pylatex import Document, Section, Subsection, Table, Math
from pylatex.utils import italic

doc = Document()
section = Section('Yaay the first section, it can even be ' + italic('italic'))

math = Math(data=['2*3', '=', 6])

section.append('This is a math function')
section.append(math)

table = Table('r|ccl')
table.add_hline()
table.add_row((1, 2, 3, 4))
table.add_hline(1, 2)
table.add_empty_row()
table.add_row((4, 5, 6, 7))

section.append(Subsection('Table of something'))
section.append(table)

doc.append(section)

doc.generate_pdf()
