# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from pylatex.base_classes import LatexObject, Environment, Command
from pylatex.package import Package


class TikZ(Environment):

    """Basic TikZ container class.

    :param data:

    :type data: list
    """

    container_name = 'tikzpicture'

    def __init__(self, data=None):

        packages = [Package('tikz')]

        super().__init__(data=data, packages=packages)


class Axis(Environment):

    """PGFPlots axis container class, this contains plots.

    :param data:
    :param options:

    :type data: list
    :type options: str
    """

    def __init__(self, data=None, options=None):
        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__(data=data, options=options, packages=packages)


class Plot(LatexObject):

    r"""A class representing a PGFPlot.

    :param name:
    :param func:
    :param coordinates:
    :param options:

    :type name: str
    :type func: str
    :type coordinates: list
    :type options: str

    TODO:

    options type can also be list or
        :class:`~pylatex.base_classes.command.Options` instance
    """

    def __init__(self, name=None, func=None, coordinates=None, options=None):
        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.options = options

        packages = [Package('pgfplots'), Command('pgfplotsset',
                                                 'compat=newest')]

        super().__init__(packages=packages)

    def dumps(self):
        """Represent the plot as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

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
