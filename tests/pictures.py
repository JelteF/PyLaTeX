#!/usr/bin/env python

from pylatex import Document, Section
from pylatex.graphics import Figure
import os


def test():
    doc = Document()
    section = Section('Multirow Test')
    figure = Figure()
    image_filename = os.path.join(os.path.dirname(__file__),
                                  '../examples/kitten.jpg')
    figure.add_image(image_filename)
    figure.add_caption('Whoooo an imagage of a pdf')
    section.append(figure)
    doc.append(section)

    doc.generate_pdf()
