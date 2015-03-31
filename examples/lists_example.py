#!/usr/bin/python
# -*- coding: utf-8 -*-

# Test for list structures in PyLaTeX.
# More info @ http://en.wikibooks.org/wiki/LaTeX/List_Structures

from pylatex import Document, Section, Itemize, Enumerate, Description


doc = Document()

# create a bulleted "itemize" list like the below:
# \begin{itemize}
#   \item The first item
#   \item The second item
#   \item The third etc \ldots
# \end{itemize}

with doc.create(Section('"Itemize" list')):
    with doc.create(Itemize()) as enum:
        enum.add_item("the first item")
        enum.add_item("the second item")
        enum.add_item("the third etc \\ldots")

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
    with doc.create(Description()) as enum:
        enum.add_item("First", "The first item")
        enum.add_item("Second", "The second item")
        enum.add_item("Third", "The third etc \\ldots")

doc.generate_pdf()
