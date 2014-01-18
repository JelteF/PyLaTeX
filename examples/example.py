#!/usr/bin/python3

import numpy as np

from pylatex import Document, Section, Subsection, Table, Math
from pylatex.numpy import Matrix
from pylatex.utils import italic

doc = Document()
section = Section('Yaay the first section, it can even be ' + italic('italic'))

section.append('Some regular text')

math = Subsection('Math', data=[Math(data=['2*3', '=', 6])])

section.append(math)
table = Table('rc|cl')
table.add_hline()
table.add_row((1, 2, 3, 4))
table.add_hline(1, 2)
table.add_empty_row()
table.add_row((4, 5, 6, 7))

table = Subsection('Table of something', data=[table])

section.append(table)

a = np.array([[100, 10, 20]]).T
M = np.matrix([[2, 3, 4],
               [0, 0, 1],
               [0, 0, 2]])

math = Math(data=[Matrix(M), Matrix(a), '=', Matrix(M*a)])
equation = Subsection('Matrix equation', data=[math])

section.append(equation)

doc.append(section)

doc.generate_pdf()
