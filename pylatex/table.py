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
from .command import Command

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

    def __init__(self, table_spec, data=None, pos=None, packages=None):
        self.table_type = 'tabular'
        self.table_spec = table_spec
        self.pos = pos

        self.width = get_table_width(table_spec)

        super().__init__(data=data, packages=packages)

    def add_hline(self, start=None, end=None):
        """Add a horizontal line to the table"""
        if start is None and end is None:
            self.append(r'\hline')
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width
            self.append(Command('cline', str(start) + '-' + str(end)))

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
        self.append(Command('multicolumn', arguments=(size, align, content)))
        if cells is not None:
            self.add_row(cells)
        else:
            self.append(r'\\')

    def add_multirow(self, size, align, content, hlines=True, cells=None,
                     escape=False):
        """
        Add a multirow of height size to the table, with cell content content
        """
        self.append(Command('multirow', arguments=(size, align, content)))
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
        string = r'\begin{' + self.table_type + '}'

        if self.pos is not None:
            string += '[' + self.pos + ']'

        string += '{' + self.table_spec + '}\n'

        string += dumps_list(self)

        string += r'\end{' + self.table_type + '}'

        super().dumps()
        return string


class Tabu(Table):

    """A class that represents a tabu (more flexible table)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, packages=[Package('tabu')], **kwargs)
        self.table_type = 'tabu'


class LongTable(Table):

    """A class that represents a longtable (multipage table)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, packages=[Package('longtable')], **kwargs)
        self.table_type = 'longtable'


class LongTabu(Table):

    """A class that represents a longtabu (more flexible multipage table)"""

    def __init__(self, *args, **kwargs):
        packages = [Package('tabu'), Package('longtable')]
        super().__init__(*args, packages=packages, **kwargs)
        self.table_type = 'longtabu'
