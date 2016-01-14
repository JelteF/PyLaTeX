# -*- coding: utf-8 -*-
r"""A test to make sure the document compiles with lmodern set to `False`."""

from pylatex import Document

doc = Document('no_lmodern', lmodern=False)
doc.append('test text')

doc.generate_pdf(clean=True, clean_tex=False, silent=False)
