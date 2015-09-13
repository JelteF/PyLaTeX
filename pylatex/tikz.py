# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from pylatex.base_classes import LatexObject, Environment, Command
from pylatex.package import Package


class TikZ(Environment):

    """Basic TikZ container class."""

    container_name = 'tikzpicture'

    def __init__(self, **kwargs):

        packages = [Package('tikz')]

        super().__init__(packages=packages, *kwargs)


class Axis(Environment):

    """PGFPlots axis container class, this contains plots."""

    def __init__(self, data=None, options=None):
        """.

        Args
        ----
        options: str, list or `~.Options`
            Options to format the axis environment.
        """
        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__(data=data, options=options, packages=packages)


class Plot(LatexObject):

    """A class representing a PGFPlot."""

    def __init__(self, name=None, func=None, coordinates=None,
                 error_bar=None, options=None):
        """.

        Args
        ----
        name: str
            Name of the plot.
        func: str
            A function that should be plotted.
        coordinates: list
            A list of exact coordinates tat should be plotted.

        options: str, list or `~.Options`
        """

        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.error_bar = error_bar
        self.options = options

        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__(packages=packages)

    def dumps(self):
        """Represent the plot as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        string = Command('addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += ' coordinates {\n'

            if self.error_bar is None:
                for x, y in self.coordinates:
                    # ie: "(x,y)"
                    string += '(' + str(x) + ',' + str(y) + ')\n'

            else:
                for (x, y), (e_x, e_y) in zip(self.coordinates,
                                              self.error_bar):
                    # ie: "(x,y) +- (e_x,e_y)"
                    string += '(' + str(x) + ',' + str(y) + \
                        ') +- (' + str(e_x) + ',' + str(e_y) + ')\n'

            string += '};\n\n'

        elif self.func is not None:
            string += '{' + self.func + '};\n\n'

        if self.name is not None:
            string += Command('addlegendentry', self.name).dumps()

        super().dumps()

        return string
