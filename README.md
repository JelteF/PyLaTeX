PyLaTeX
=======

PyLaTeX is a Python library for creating LaTeX files. The point of this library
is being an easy, but extensible interface between Python and LaTeX.


### Features

The library contains some basic features I have had the need for so far.
Currently those are:

- Document generation and compilation
- Section, table and package classes
- An escape function
- Bold and italic functions

Everything else you want you can still add to the document by adding LaTeX
formatted strings instead of classes or regular strings.


### Dependencies

- Python 3.3 (Python 3.x might work as well)
- pdflatex (only if you want to compile the tex file)


### Installation
`pip install pylatex`


### Example

```python
from pylatex import Document, Section, Table
from pylatex.utils import italic

doc = Document()
section = Section('Yaay the first section, it can even be ' + italic('italic'))

table = Table('r|ccl')
table.add_hline()
table.add_row((1, 2, 3, 4))
table.add_hline(1, 2)
table.add_empty_row()
table.add_row((4, 5, 6, 7))

section.content.append(table)
doc.content.append(section)
doc.generate_pdf()
```

This code will generate this:
![Generated PDF by PyLaTeX](https://raw.github.com/JelteF/PyLaTeX/master/docs/static/screenshot.png)


### Future development

I will keep adding functionality I need to this library, an interface for
graphics and math will probably be added in a future version.

If you add a feature yourself, or fix a bug, please send a pull request.

You can submit issues, but it will not be my priority to fix them. My job and
education are a bit higher on the priority list.


### Support

This library is being developed for Python 3.3. It currently doesn't work for
Python 2.7, but it's mostly syntax and import changes that break it for 2.7.
It is also only tested on Linux, so it might not work on any different
platforms.

I have no intention of testing on any different platforms or with different
Python versions. I also don't have the intention to write fixes for platform or
environment specific bugs, but pull requests that fix those are always welcome.


### Copyright and License

Copyright 2014 Jelte Fennema, under [the MIT
license](https://github.com/JelteF/PyLaTeX/blob/master/LICENSE)
