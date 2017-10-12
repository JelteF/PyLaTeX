# -*- coding: utf-8 -*-
r"""A test to make sure the document compiles with inputenc set to `None`."""

from pylatex.base_classes import Arguments
from pylatex import Document

doc = Document('no_inputenc', inputenc=None)
doc.append('test text')

# Make sure inputenc isn't used
assert not any([p.arguments == Arguments('inputenc') for p in doc.packages])

doc.generate_pdf(clean=True, clean_tex=False, silent=False)
