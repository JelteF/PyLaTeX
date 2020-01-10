#!/usr/bin/python
"""
This example shows TikZ drawing capabilities.

..  :copyright: (c) 2017 by Bruno Morais
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import (Document, TikZ, TikZNode, TikZDraw, TikZCoordinate,
                     TikZPolarCoordinate, TikZCoordinateVariable,
                     TikZUserPath, TikZOptions, NoEscape, TikZScope,
                     TikZArc)
from pylatex.tikz import TikZLibrary

if __name__ == '__main__':

    # create document
    doc = Document()

    # can manually add tikz libraries to document
    # (some are detected automatically, like calc)
    doc.preamble.append(TikZLibrary("arrows.meta"))
    doc.preamble.append(TikZLibrary("decorations.markings"))

    # add our sample drawings
    with doc.create(TikZ()) as pic:

        # options for our node
        node_kwargs = {'align': 'center',
                       'minimum size': '100pt',
                       'fill': 'black!20'}

        # create our test node
        box = TikZNode(text='My block',
                       handle='box',
                       options=TikZOptions('draw',
                                           'rounded corners',
                                           **node_kwargs))

        # add to tikzpicture
        pic.append(box)

        # draw a few paths
        pic.append(TikZDraw([TikZCoordinate(0, -6),
                             'rectangle',
                             TikZCoordinate(2, -8)],
                            options=TikZOptions(fill='red')))

        # show use of anchor, relative coordinate
        pic.append(TikZDraw([box.west,
                             '--',
                             '++(-1,0)']))

        # demonstrate the use of the with syntax
        with pic.create(TikZDraw()) as path:

            # start at an anchor of the node
            path.append(box.east)

            # necessary here because 'in' is a python keyword
            path_options = {'in': 90, 'out': 0}
            path.append(TikZUserPath('edge',
                                     TikZOptions('-latex', **path_options)))
            path.append(TikZCoordinate(1, 0, relative=True))

        # Demonstrate use of arc syntax and \coordinate variables with
        # TikZ Scopes. Example is drawing an integration contour diagram
        # with an isolated singularity:

        # define a coordinate so that we can reposition the origin easily
        # after the latex is produced
        orig = TikZCoordinateVariable(handle="orig", at=TikZCoordinate(5, -3))
        orig_handle = orig.get_handle()  # handle label to coordinate
        pic.append(orig)  # add definition of coordinate

        # demonstrate use of tikz scopes
        scope_options = TikZOptions(
            NoEscape("decoration={markings," "\n" r"mark=between positions 0.1"
                     r" and 0.9 step 0.25 with {\arrow[very thick]{>}},}"
                     "\n"), shift=orig_handle, scale=2)

        with doc.create(TikZScope(options=scope_options)) as scope:
            draw_options = TikZOptions(fill="gray!10", postaction="decorate", )
            rad = 1
            sing_rad = 0.25
            # angle constants
            s = 0
            f = 180
            scope.append(
                TikZDraw([TikZPolarCoordinate(angle=s, radius=rad),
                          'arc', TikZArc(s, f, rad),
                          '--', TikZPolarCoordinate(f, sing_rad),
                          'arc', TikZArc(f, s, sing_rad),
                          '--', 'cycle'],  # close shape with cycle
                         options=draw_options))

        # demonstrate the use of \coordinate variables without scope

        # (Add an axis to diagram):

        rad = 3.5
        draw_options = TikZOptions("very thick", "->")
        # can handle addition/ subtraction between coordinate handle
        # & explicit coordinate object.

        # can also use node in draw inline context
        pic.append(TikZDraw([orig_handle + TikZCoordinate(-rad, 0), '--',
                            orig_handle + TikZCoordinate(rad, 0),
                            TikZNode(text=NoEscape("{$\Re$}"),
                                     options=['above'])],
                            options=draw_options))
        pic.append(TikZDraw([orig_handle + TikZCoordinate(0, -rad), '--',
                            orig_handle + TikZCoordinate(0, rad),
                            TikZNode(text=NoEscape("{$\Im$}"),
                                     options=['right'])],
                            options=draw_options))
    doc.generate_pdf('tikzdraw', clean_tex=False)
