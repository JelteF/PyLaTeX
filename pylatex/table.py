# -*- coding: utf-8 -*-
"""
    pylatex.table
    ~~~~~~~

    This module implements the class that deals with tables.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import BaseLaTeXContainer
from .package import Package

from collections import Counter
import re


def get_table_width(table_spec):
    column_letters = ['l', 'c', 'r', 'p', 'm', 'b']

    # Remove things like {\bfseries}
    cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)
    spec_counter = Counter(cleaner_spec)

    return sum(spec_counter[l] for l in column_letters)


class Table(BaseLaTeXContainer):

    """A class that represents a table."""

    def __init__(self, table_spec, data=None, pos=None):
        self.table_spec = table_spec
        self.pos = pos

        self.width = get_table_width(table_spec)

        super().__init__(data)

    def add_hline(self, start=None, end=None):
        """Add a horizontal line to the table"""
        if start is None and end is None:
            self.append(r'\hline')
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width
            self.append(r'\cline{' + str(start) + '-' + str(end) + '}')

    def add_empty_row(self):
        """Add an empty row to the table"""
        self.append((self.width - 1) * '&' + r'\\')

    def add_row(self, cells, escape=False):
        """Add a row of cells to the table"""
        self.append(dumps_list(cells, escape=escape, token='&') + r'\\')

    def add_multicolumn(self, size, align, content, cells=None, escape=False):
        """
        Add a multicolumn of width size to the table, with cell content content
        """
        self.append(r'\multicolumn{%d}{%s}{%s}' % (size, align, content))
        if cells is not None:
            self.add_row(cells)
        else:
            self.append(r'\\')

    def add_multirow(self, size, align, content, hlines=True, cells=None,
                     escape=False):
        """
        Add a multirow of height size to the table, with cell content content
        """
        self.append(r'\multirow{%d}{%s}{%s}' % (size, align, content))
        self.packages.add(Package('multirow'))
        if cells is not None:
            for i, row in enumerate(cells):
                if hlines and i:
                    self.add_hline(2)
                self.append('&')
                self.add_row(row)
        else:
            for i in range(size):
                self.add_empty_row()

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        string = r'\begin{tabular}'

        if self.pos is not None:
            string += '[' + self.pos + ']'

        string += '{' + self.table_spec + '}\n'

        string += dumps_list(self)

        string += r'\end{tabular}'

        super().dumps()
        return string
