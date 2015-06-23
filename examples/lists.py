#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This example shows list functionality.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
# Test for list structures in PyLaTeX.
# More info @ http://en.wikibooks.org/wiki/LaTeX/List_Structures
from pylatex import Document, Section, Itemize, Enumerate, Description

if __name__ == '__main__':
    doc = Document()

    # create a bulleted "itemize" list like the below:
    # \begin{itemize}
    #   \item The first item
    #   \item The second item
    #   \item The third etc \ldots
    # \end{itemize}

    with doc.create(Section('"Itemize" list')):
        with doc.create(Itemize()) as itemize:
            itemize.add_item("the first item")
            itemize.add_item("the second item")
            itemize.add_item("the third etc")
            itemize.append("\\ldots")  # you can append to existing items

    # create a numbered "enumerate" list like the below:
    # \begin{enumerate}
    #   \item The first item
    #   \item The second item
    #   \item The third etc \ldots
    # \end{enumerate}

    with doc.create(Section('"Enumerate" list')):
        with doc.create(Enumerate()) as enum:
            enum.add_item("the first item")
            enum.add_item("the second item")
            enum.add_item("the third etc \\ldots")

    # create a labelled "description" list like the below:
    # \begin{description}
    #   \item[First] The first item
    #   \item[Second] The second item
    #   \item[Third] The third etc \ldots
    # \end{description}

    with doc.create(Section('"Description" list')):
        with doc.create(Description()) as desc:
            desc.add_item("First", "The first item")
            desc.add_item("Second", "The second item")
            desc.add_item("Third", "The third etc \\ldots")

    doc.generate_pdf()
