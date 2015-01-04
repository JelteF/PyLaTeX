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
from pylatex.command import Command


class TikZ(BaseLaTeXNamedContainer):

    """Basic TikZ container class."""

    def __init__(self, data=None):
        packages = [Package('tikz')]
        super().__init__('tikzpicture', data=data, packages=packages)


class Axis(BaseLaTeXNamedContainer):

    """PGFPlots axis container class, this contains plots."""

    def __init__(self, data=None, options=None):
        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__('axis', data=data, options=options, packages=packages)


class Plot(BaseLaTeXClass):

    """PGFPlot normal plot."""

    def __init__(self, name=None, func=None, coordinates=None, options=None):
        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.options = options

        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__(packages=packages)

    def dumps(self):
        """Represents the plot as a string in LaTeX syntax."""
        string = Command('addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += ' coordinates {\n'

            for x, y in self.coordinates:
                string += '(' + str(x) + ',' + str(y) + ')\n'
            string += '};\n\n'

        elif self.func is not None:
            string += '{' + self.func + '};\n\n'

        if self.name is not None:
            string += Command('addlegendentry', self.name).dumps()

        super().dumps()

        return string
