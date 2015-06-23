# -*- coding: utf-8 -*-
"""
This module implements the base class for table classes.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from . import LatexObject, Environment, Command
from ..utils import dumps_list
from ..package import Package


from collections import Counter
import re


def get_table_width(table_spec):
    """Calculate the width of a table based on its spec.

    :param table_spec:

    :type table_spec: str

    :return:
    :rtype: int
    """

    # TODO make this function private

    column_letters = ['l', 'c', 'r', 'p', 'm', 'b']

    # Remove things like {\bfseries}
    cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)
    spec_counter = Counter(cleaner_spec)

    return sum(spec_counter[l] for l in column_letters)


class TabularBase(Environment):

    """A class that is used as a base for all table classes.

    :param table_spec:
    :param data:
    :param pos:

    :type table_spec: str
    :type data: list
    :type pos: list
    """

    def __init__(self, table_spec, data=None, pos=None, **kwargs):
        self.width = get_table_width(table_spec)

        super().__init__(data=data, options=pos,
                         argument=table_spec, **kwargs)

    def add_hline(self, start=None, end=None):
        """Add a horizontal line to the table.

        :param start:
        :param end:

        :type start: int
        :type end: int
        """

        if start is None and end is None:
            self.append(r'\hline')
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width

            self.append(Command('cline', str(start) + '-' + str(end)))

    def add_empty_row(self):
        """Add an empty row to the table."""

        self.append((self.width - 1) * '&' + r'\\')

    def add_row(self, cells, escape=False):
        """Add a row of cells to the table.

        :param cells:
        :param escape:

        :type cells: tuple
        :type escape: bool
        """

        # Propegate packages used in cells
        for c in cells:
            if isinstance(c, LatexObject):
                for p in c.packages:
                    self.packages.add(p)

        self.append(dumps_list(cells, escape=escape, token='&') + r'\\')

    def add_multicolumn(self, size, align, content, cells=None, escape=False):
        """Add a multicolumn of width size to the table, with cell content.

        :param size:
        :param align:
        :param content:
        :param cells:
        :param escape:

        :type size: int
        :type align: str
        :type content: str
        :type cells: tuple
        :type escape: bool
        """

        self.append(Command('multicolumn', arguments=(size, align, content)))

        if cells is not None:
            self.add_row(cells)
        else:
            self.append(r'\\')

    def add_multirow(self, size, align, content, hlines=True, cells=None,
                     escape=False):
        """Add a multirow of height size to the table, with cell content.

        :param size:
        :param align:
        :param content:
        :param hlines:
        :param cells:
        :param escape:

        :type size: int
        :type align: str
        :type content: str
        :type hlines: bool
        :type cells: tuple
        :type escape: bool
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
