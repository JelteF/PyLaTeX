#!/usr/bin/env python

from pylatex import Document, Section
from pylatex.graphics import Figure


def test():
    doc = Document()
    section = Section('Multirow Test')
    figure = Figure()
    figure.add_image('docs/source/_static/screenshot.png')
    figure.add_caption('Whoooo an imagage of a pdf')
    section.append(figure)
    doc.append(section)

    doc.generate_pdf()
