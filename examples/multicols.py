#!/usr/bin/env python3
"""This example shows the multicols functionality."""

from pylatex import Document, Section, Itemize, MultiCols

if __name__ == '__main__':
    doc = Document()

    # create a bulleted "itemize" list inside a 2 column mutlicols like the below:
    # \begin{itemize}
    #   \item The first item
    #   \item The second item
    #   \item The third etc \ldots
    # \end{itemize}

    with doc.create(Section('2 column list')):
        with doc.create(MultiCols(2)):
            with doc.create(Itemize()) as itemize:
                itemize.add_item("the first item")
                itemize.add_item("the second item")
                itemize.add_item("the third etc")

    doc.generate_pdf('multicols', clean_tex=False)
