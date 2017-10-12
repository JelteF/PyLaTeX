# -*- coding: utf-8 -*-
r"""A test to make sure the document compiles with fontenc set to `None`."""

from pylatex.base_classes import Arguments
from pylatex import Document

doc = Document('no_fontenc', fontenc=None)
doc.append('test text')

# Make sure fontenc isn't used
assert not any([p.arguments == Arguments('fontenc') for p in doc.packages])

doc.generate_pdf(clean=True, clean_tex=False, silent=False)
