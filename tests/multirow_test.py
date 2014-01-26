#!/usr/bin/python3

import numpy as np

from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot
from pylatex.numpy import Matrix
from pylatex.utils import italic

doc = Document(filename="multirow")
section = Section('Multirow Test')

test1 = Subsection('Multicol')
test2 = Subsection('Multirow')

table1 = Table('|c|c|')
table1.add_hline()
table1.add_multicolumn(2, '|c|', 'Multicol')
table1.add_hline()
table1.add_row((1, 2))
table1.add_hline()
table1.add_row((3, 4))
table1.add_hline()

table2 = Table('|cc|c|c|')
table2.add_hline()
table2.add_multirow(2, '*', 'Multirow', cells=((1, 2), (3, 4)))
table2.add_hline()

test1.append(table1)
test2.append(table2)

section.append(test1)
section.append(test2)

doc.append(section)
doc.generate_tex()
doc.generate_pdf()
