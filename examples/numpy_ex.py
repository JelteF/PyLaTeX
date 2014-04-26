#!/usr/bin/python3

import numpy as np

from pylatex import Document, Section, Subsection, Table, Math
from pylatex.numpy import Matrix, format_vec


a = np.array([[100, 10, 20]]).T

doc = Document(filename="numpy_ex")
section = Section('Numpy tests')
subsection = Subsection('Array')

vec = Matrix(a)
vec_name = format_vec('a')
math = Math(data=[vec_name, '=', vec])

subsection.append(math)
section.append(subsection)

subsection = Subsection('Matrix')
M = np.matrix([[2, 3, 4],
               [0, 0, 1],
               [0, 0, 2]])
matrix = Matrix(M, mtype='b')
math = Math(data=['M=', matrix])

subsection.append(math)
section.append(subsection)


subsection = Subsection('Product')

math = Math(data=['M', vec_name, '=', Matrix(M*a)])
subsection.append(math)

section.append(subsection)

doc.append(section)
doc.generate_pdf()
