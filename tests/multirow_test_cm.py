#!/usr/bin/python

from pylatex import Document, Section, Subsection, Tabular

doc = Document("multirow")

with doc.create(Section('Multirow Test')):
    with doc.create(Subsection('Multicol')):
        # we need to keep track of the object here
        with doc.create(Tabular('|c|c|')) as table1:
            table1.add_hline()
            table1.add_multicolumn(2, '|c|', 'Multicol')
            table1.add_hline()
            table1.add_row((1, 2))
            table1.add_hline()
            table1.add_row((3, 4))
            table1.add_hline()

    with doc.create(Subsection('Multirow')):
        with doc.create(Tabular('|c|c|c|')) as table2:
            table2.add_hline()
            table2.add_multirow(3, '*', 'Multirow', cells=((1, 2), (3, 4),
                                                           (5, 6)))
            table2.add_hline()
            table2.add_multirow(3, '*', 'Multirow2')
            table2.add_hline()

doc.generate_pdf()
