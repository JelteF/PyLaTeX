# -*- coding: utf-8 -*-
"""
This module implements the base class for table classes.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from . import LatexObject, Environment, Command
from ..utils import dumps_list, NoEscape


from collections import Counter
import re


def _get_table_width(table_spec):
    """Calculate the width of a table based on its spec.

    Args
    ----
    table_spec: str
        The LaTeX column specification for a table.


    Returns
    -------
    int
        The width of a table which uses the specification supplied.
    """

    column_letters = ['l', 'c', 'r', 'p', 'm', 'b']

    # Remove things like {\bfseries}
    cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)
    spec_counter = Counter(cleaner_spec)

    return sum(spec_counter[l] for l in column_letters)


class TabularBase(Environment):
    """A class that is used as a base for all table classes."""

    def __init__(self, table_spec, data=None, pos=None, **kwargs):
        """.

        Args
        ----
        table_spec: str
            A string that represents how many columns a table should have and
            if it should contain vertical lines and where.
        pos: list

        References
        ----------
        * https://en.wikibooks.org/wiki/LaTeX/Tables#The_tabular_environment
        """

        self.width = _get_table_width(table_spec)

        super().__init__(data=data, options=pos,
                         arguments=table_spec, **kwargs)

    def add_hline(self, start=None, end=None):
        """Add a horizontal line to the table.

        Args
        ----
        start: int
            At what cell the line should begin
        end: int
            At what cell the line should end
        """

        if start is None and end is None:
            self.append(NoEscape(r'\hline'))
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width

            self.append(Command('cline', str(start) + '-' + str(end)))

    def add_empty_row(self):
        """Add an empty row to the table."""

        self.append(NoEscape((self.width - 1) * '&' + r'\\'))

    def add_row(self, cells, escape=None, mapper=None):
        """Add a row of cells to the table.

        Args
        ----
        cells: iterable, such as a `list` or `tuple`
            Each element of the iterable will become a the content of cell.
        """

        if escape is None:
            escape = self.escape

        # Propegate packages used in cells
        for c in cells:
            if isinstance(c, LatexObject):
                for p in c.packages:
                    self.packages.add(p)

        self.append(dumps_list(cells, escape=escape, token='&', mapper=mapper)
                    + NoEscape(r'\\'))
