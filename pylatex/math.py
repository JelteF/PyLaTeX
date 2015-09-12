# -*- coding: utf-8 -*-
'''
This module implements the classes that deal with math.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
'''

from .base_classes import LatexObject, Command, Container
from pylatex.package import Package


class Math(Container):

    '''A class representing a math environment.'''

    def __init__(self, data=None, inline=False):
        '''.

        Args
        ----
        data: list
            Content of the math container.
        inline: bool
            If the math should be displayed inline or not.
        '''

        self.inline = inline
        super().__init__(data)

    def dumps(self):
        '''Return a LaTeX formatted string representing the object.

        Returns
        -------
        str

        '''

        if self.inline:
            string = '$' + super().dumps(token=' ') + '$'
        else:
            string = '$$' + super().dumps(token=' ') + '$$\n'

        super().dumps()

        return string


class VectorName(Command):

    '''A class representing a named vector.'''

    def __init__(self, name):
        '''.

        Args
        ----
        name: str
            Name of the vector
        '''

        super().__init__('mathbf', arguments=name)


class Matrix(LatexObject):

    '''A class representing a matrix.'''

    # TODO: Convert this to an environment

    def __init__(self, matrix, mtype='p', alignment=None):
        r'''.

        Args
        ----
        matrix: `numpy.ndarray` instance
            The matrix to display
        mtype: str
            What kind of brackets are used around the matrix. The different
            options and their corresponding brackets are:
            p = ( ), b = [ ], B = { }, v = \| \|, V = \|\| \|\|
        alignment: str
            How to align the content of the cells in the matrix. This is ``c``
            by default.

        References
        ----------
        * https://en.wikibooks.org/wiki/LaTeX/Mathematics#Matrices_and_arrays
        '''

        import numpy as np
        self._np = np

        self.mtype = mtype
        self.matrix = matrix
        self.alignment = alignment

        super().__init__(packages=[Package('amsmath')])

    def dumps(self):
        '''Return a string representin the matrix in LaTeX syntax.

        Returns
        -------
        str
        '''

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

        for (y, x), value in self._np.ndenumerate(self.matrix):
            if x:
                string += '&'
            string += str(value)

            if x == shape[1] - 1 and y != shape[0] - 1:
                string += r'\\' + '\n'

        string += '\n'

        string += r'\end{' + mtype + '}'

        super().dumps()

        return string
