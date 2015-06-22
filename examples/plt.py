#!/usr/bin/python
"""
    Matplotlib example
    ~~~~~~~~~~~~~~~~~~

    This example shows matplotlib functionality.

    .. literalinclude:: /../../examples/plt.py
        :start-after: begin-doc-include
        :lines: 10-

    ..  :copyright: (c) 2014 by Jelte Fennema.
        :license: MIT, see License for more details.
"""

# begin-doc-include
import matplotlib
matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot

from pylatex import Document, Package, Section, Plt


def main(fname, width, *args, **kwargs):
    doc = Document(fname)
    doc.packages.append(Package('geometry', options=['left=2cm', 'right=2cm']))

    doc.append('Introduction.')

    with doc.create(Section('I am a section')):
        doc.append('Take a look at this beautiful plot:')

        with doc.create(Plt(position='htbp')) as plot:
            plot.add_plot(pyplot, width=width, *args, **kwargs)
            plot.add_caption('I am a caption.')

        doc.append('Created using matplotlib.')

    doc.append('Conclusion.')

    doc.generate_pdf()


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    pyplot.plot(x, y)

    main('plt_dpi', r'1\textwidth', dpi=300)
    main('plt_facecolor', r'0.5\textwidth', facecolor='b')
