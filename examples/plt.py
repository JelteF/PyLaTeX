#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot

from pylatex import Document, Section, Plt


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    pyplot.plot(x, y)

    doc = Document('matplolib_pdf')
    doc.append('Introduction.')

    with doc.create(Section('I am a section')):
        doc.append('Take a look at this beautiful plot:')

        with doc.create(Plt(position='htbp')) as plot:
            plot.add_plot(pyplot)
            plot.add_caption('I am a caption.')

        doc.append('Created using matplotlib.')

    doc.append('Conclusion.')

    doc.generate_pdf()
