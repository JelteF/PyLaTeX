# -*- coding: utf-8 -*-
"""
This module implements the classes that deals with numpy objects.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import numpy as np
from .base_classes import LatexObject, Command
from pylatex.package import Package


class VectorName(Command):

    """A class representing a named vector.

    :param name:

    :type name: str
    """

    def __init__(self, name):
        super().__init__('mathbf', arguments=name)


class Matrix(LatexObject):

    """A class representing a matrix.

    :param matrix:
    :param name:
    :param mtype:
    :param alignment:

    :type matrix: :class:`numpy.ndarray` instance
    :type name: str
    :type mtype: str
    :type alignment: str
    """

    def __init__(self, matrix, name='', mtype='p', alignment=None):
        self.mtype = mtype
        self.matrix = matrix
        self.alignment = alignment
        self.name = name

        super().__init__(packages=[Package('amsmath')])

    def dumps(self):
        """Return a string representin the matrix in LaTeX syntax.

        :rtype: str
        """

        string = r'\begin{'
        mtype = self.mtype + 'matrix'

        if self.alignment is not None:
            mtype += '*'
            alignment = '{' + self.alignment + '}'
        else:
            alignment = ''

        string += mtype + '}' + alignment
        string += '\n'

        shape = self.matrix.shape

        for (y, x), value in np.ndenumerate(self.matrix):
            if x:
                string += '&'
            string += str(value)

            if x == shape[1] - 1 and y != shape[0] - 1:
                string += r'\\' + '\n'

        string += '\n'

        string += r'\end{' + mtype + '}'

        super().dumps()

        return string
