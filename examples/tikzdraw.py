#!/usr/bin/python
"""
This example shows TikZ drawing capabilities.

    :license: MIT, see License for more details.
"""

from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions)

if __name__ == '__main__':

    # create document
    doc = Document()

    # add our sample drawings
    with doc.create(TikZ()) as pic:

        # options for our node
        node_kwargs = {'align': 'center',
                       'minimum size': '100pt'}

        # create our test node
        box = TikZNode(text='My block',
                       handle='box',
                       options=TikZOptions('draw',
                                           'rounded corners',
                                           **node_kwargs))

        # add to tikzpicture
        pic.append(box)

        # draw a few paths
        pic.append(TikZDraw([TikZCoordinate(0, 0),
                             '--',
                             TikZCoordinate(0, 1)]))

        # show use of anchor, relative coordinate
        pic.append(TikZDraw([box.west,
                             '--',
                             '++(-1,0)']))

        # demonstrate the use of the with syntax
        with pic.create(TikZDraw(options=TikZOptions('->'))) as path:

            # start at an anchor of the node
            path.append(box.east)

            # necessary here because 'in' is a python keyword
            path_options = {'in': 90, 'out': 0}
            path.append(TikZUserPath('edge',
                                     TikZOptions(**path_options)))

            path.append(TikZCoordinate(1, 0, relative=True))

    doc.generate_pdf('tikzdraw')
