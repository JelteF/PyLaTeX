#!/usr/bin/env python

from pylatex import Document, Section
from pylatex.utils import escape_latex

doc = Document(default_filename="utils_escape_latex")
section = Section('Escape LaTeX characters test')

text = escape_latex('''\
& (ampersand)
% (percent)
$ (dollar)
# (number)
_ (underscore)
{ (left curly brace)
} (right curly brace)
~ (tilde)
^ (caret)
\\ (backslash)
''')

section.append(text)
doc.append(section)

doc.generate_pdf()
