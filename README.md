PyLaTeX
=======

PyLaTeX is a Python library for creating LaTeX files. The goal of this library
is being an easy, but extensible interface between Python and LaTeX.


### Features

The library contains some basic features I have had the need for so far.
Currently those are:

- Document generation and compilation
- Section, table, math and package classes
- A matrix class that can compile NumPy ndarrays and matrices to LaTeX
- An escape function
- Bold and italic functions
- Every class has a dump method, which writes the output to a filepointer

Everything else you want you can still add to the document by adding LaTeX
formatted strings instead of classes or regular strings.


### Dependencies

- Python 3.x or Python 2.7
- pdflatex (only if you want to compile the tex file)
- NumPy (only if you want to convert it's matrixes)
- ordered-set


### Installation
`pip install pylatex`


### Examples

```python
import numpy as np

from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Package
from pylatex.numpy import Matrix
from pylatex.utils import italic, escape_latex

doc = Document()
doc.packages.append(Package('geometry', options=['tmargin=1cm',
                                                 'lmargin=10cm']))

with doc.create(Section('The simple stuff')):
    doc.append('Some regular text and some ' + italic('italic text. '))
    doc.append(escape_latex('\nAlso some crazy characters: $&#{}'))
    with doc.create(Subsection('Math that is incorrect')) as math:
        doc.append(Math(data=['2*3', '=', 9]))

    with doc.create(Subsection('Table of something')):
        with doc.create(Table('rc|cl')) as table:
            table.add_hline()
            table.add_row((1, 2, 3, 4))
            table.add_hline(1, 2)
            table.add_empty_row()
            table.add_row((4, 5, 6, 7))

a = np.array([[100, 10, 20]]).T
M = np.matrix([[2, 3, 4],
               [0, 0, 1],
               [0, 0, 2]])

with doc.create(Section('The fancy stuff')):
    with doc.create(Subsection('Correct matrix equations')):
        doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M*a)]))

    with doc.create(Subsection('Beautiful graphs')):
        with doc.create(TikZ()):
            plot_options = 'height=6cm, width=6cm, grid=major'
            with doc.create(Axis(options=plot_options)) as plot:
                plot.append(Plot(name='model', func='-x^5 - 242'))

                coordinates = [
                    (-4.77778, 2027.60977),
                    (-3.55556, 347.84069),
                    (-2.33333, 22.58953),
                    (-1.11111, -493.50066),
                    (0.11111, 46.66082),
                    (1.33333, -205.56286),
                    (2.55556, -341.40638),
                    (3.77778, -1169.24780),
                    (5.00000, -3269.56775),
                ]

                plot.append(Plot(name='estimate', coordinates=coordinates))

    with doc.create(Subsection('Cute kitten pictures')):
        with doc.create(Figure(position='h!')) as kitten_pic:
            kitten_pic.add_image('docs/static/kitten.jpg', width='120px')
            kitten_pic.add_caption('Look it\'s on its back')

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

This library is being developed in and for Python 3. Because of a conversion
script the current version also works in Python 2.7. For future versions, no
such promise will be made. Uncompatible Python 3 features will not be headed to
keep supporting Python 2.7.

The platform this library is developed for is Linux. I have no intention to
write fixes or test for platform specific bugs. Pull requests that fix those
are always welcome though.


### Copyright and License

Copyright 2014 Jelte Fennema, under [the MIT
license](https://github.com/JelteF/PyLaTeX/blob/master/LICENSE)
