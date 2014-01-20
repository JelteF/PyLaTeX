# -*- coding: utf-8 -*-
"""
    pylatex.pgfplots
    ~~~~~~~~~~~~~~~~

    This module implements the classes used to show plots.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from pylatex.base_classes import BaseLaTeXClass, BaseLaTeXNamedContainer
from pylatex.package import Package


class TikZ(BaseLaTeXNamedContainer):

    """Basic TikZ container class."""

    def __init__(self, data=None):
        packages = [Package('tikz')]
        super().__init__('tikzpicture', data=data, packages=packages)


class Axis(BaseLaTeXNamedContainer):

    """PGFPlots axis container class, this contains plots."""

    def __init__(self, data=None, options=None):
        packages = [Package('pgfplots'), Package('compat=newest',
                                                 base='pgfplotsset')]

        super().__init__('axis', data=data, options=options, packages=packages)


class Plot(BaseLaTeXClass):

    """PGFPlot normal plot."""

    def __init__(self, name=None, func=None, coordinates=None, options=None):
        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.options = options

        packages = [Package('pgfplots'), Package('compat=newest',
                                                 base='pgfplotsset')]

        super().__init__(packages=packages)

    def dumps(self):
        """Represents the plot as a string in LaTeX syntax."""
        string = r'\addplot'

        if self.options is not None:
            string += '[' + self.options + ']'

        if self.coordinates is not None:
            string += ' coordinates {\n'

            for c in self.coordinates:
                string += '(' + str(c[0]) + ',' + str(c[1]) + ')\n'
            string += '};\n\n'

        elif self.func is not None:
            string += '{' + self.func + '};\n\n'

        if self.name is not None:
            string += r'\addlegendentry{' + self.name + '}\n'

        super().dumps()

        return string
