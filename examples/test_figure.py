# -*- coding: utf-8 -*-


import numpy as np

from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot
from pylatex.float import Figure, Subfloat, Graphics, Dimension

from pylatex.utils import italic

doc = Document(filename="test_figre.tex")
section = Section(u'Yaay the first section, it can even be ' + italic(u'italic'))

figure = Figure(caption="Foo")

graphics = Graphics("example_img.jpg", width=Dimension(0.43, "textwidth"))

figure.append(Subfloat("Sub A", graphics))
figure.append(Subfloat("Sub B", graphics))
figure.new_subfig_row()
figure.append(Subfloat("Sub C", graphics))
figure.append(Subfloat("Sub D", graphics))

section.append(figure)

doc.append(section)
doc.generate_pdf(clean=False)
