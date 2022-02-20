#!/usr/bin/env python

import os

from pylatex import Document, Section
from pylatex.figure import Figure
import matplotlib.pyplot as plt


def test_add_image():
    doc = Document()
    section = Section("Add image Test")
    figure = Figure()
    image_filename = os.path.join(os.path.dirname(__file__), "../examples/kitten.jpg")
    figure.add_image(image_filename)
    figure.add_caption("Whoooo an image of a kitty")
    section.append(figure)
    doc.append(section)

    doc.generate_pdf()


def test_add_plot():
    doc = Document()
    section = Section("Add plot Test")
    mplfig = plt.figure()

    figure = Figure()
    figure.add_plot()
    figure.add_caption("Whoooo current matplotlib fig")
    section.append(figure)

    figure = Figure()
    figure.add_plot(figure=mplfig)
    figure.add_caption("Whoooo image from figure handle")
    section.append(figure)

    doc.append(section)

    doc.generate_pdf()
