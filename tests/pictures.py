#!/usr/bin/env python

from pylatex import Document, Section
from pylatex.graphics import Figure

doc = Document()
section = Section('Multirow Test')
figure = Figure()
figure.add_image('docs/static/screenshot.png')
figure.add_caption('Whoooo an imagage of a pdf')
section.append(figure)
doc.append(section)

doc.generate_pdf()
