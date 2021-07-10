#!/usr/bin/python
"""
This example shows TikZ drawing capabilities overlaying the current page.

..  :copyright: (c) 2021 by Antonio Cervone
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import (
    Document,
    TikZ,
    TikZNode,
    TikZNodeAnchor,
    TikZOptions,
)

if __name__ == "__main__":

    # create document
    doc = Document()

    # options for the tikzpicture environment
    tikz_opts = TikZOptions("remember picture", "overlay")

    # add our sample drawings
    with doc.create(TikZ(options=tikz_opts)) as pic:

        # create an anchor to the page center
        page_center = TikZNodeAnchor("current page", "center")

        # create a node on the center of the page
        centerbox = TikZNode(
            text="this is the center",
            at=page_center,
            options=TikZOptions("draw"),
        )

        # add to tikzpicture
        pic.append(centerbox)

        # create an anchor to the page center
        page_top = TikZNodeAnchor("current page", "north")

        # create a node at the top of the page
        topbox = TikZNode(
            text="this is the top", at=page_top, options=({"anchor": "north"})
        )

        # add to tikzpicture
        pic.append(topbox)

    doc.generate_pdf("tikzcp", clean_tex=False)
