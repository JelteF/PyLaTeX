# -*- coding: utf-8 -*-
"""
    pylatex.table
    ~~~~~~~

    This module implements the class that deals with tables.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import BaseLaTeXNamedContainer
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


class Table(BaseLaTeXNamedContainer):

    """A class that represents a table."""

    def __init__(self, table_spec, data=None, pos=None, table_type='tabular',
                 **kwargs):
        self.width = get_table_width(table_spec)

        super().__init__(table_type, data=data, options=pos,
                         argument=table_spec, **kwargs)

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


class Tabu(Table):

    """A class that represents a tabu (more flexible table)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table_type='tabu', packages=[Package('tabu')],
                         **kwargs)


class LongTable(Table):

    """A class that represents a longtable (multipage table)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table_type='longtable',
                         packages=[Package('longtable')], **kwargs)


class LongTabu(Table):

    """A class that represents a longtabu (more flexible multipage table)"""

    def __init__(self, *args, **kwargs):
        packages = [Package('tabu'), Package('longtable')]
        super().__init__(*args, table_type='longtabu', packages=packages,
                         **kwargs)
