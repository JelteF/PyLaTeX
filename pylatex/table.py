# -*- coding: utf-8 -*-
"""
    pylatex.table
    ~~~~~~~

    This module implements the class that deals with tables.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list

from collections import Counter
import re


class Table():

    """A class that represents a table."""

    def __init__(self, table_spec, pos=None):
        self.table_spec = table_spec
        self.pos = pos

        column_letters = ['l', 'c', 'r', 'p', 'm', 'b']

        # Remove things like {\bfseries}
        cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)
        spec_counter = Counter(cleaner_spec)

        self.width = sum(spec_counter[l] for l in column_letters)

        self.content = []

    def add_hline(self, start=None, end=None):
        """Add a horizontal line to the table"""
        if start is None and end is None:
            self.content.append(r'\hline')
        else:
            if start is None:
                start = 1
            elif end is None:
                end = self.width
            self.content.append(r'\cline{' + str(start) + '-' + str(end) + '}')

    def add_empty_row(self):
        """Add an empty row to the table"""
        self.content.append((self.width - 1) * '&' + r'\\')

    def add_row(self, cells, escape=False):
        """Add a row of cells to the table"""
        self.content.append(dumps_list(cells, escape=escape, token='&') +
                            r'\\')

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        string = r'\begin{tabular}'

        if self.pos is not None:
            string += '[' + self.pos + ']'

        string += '{' + self.table_spec + '}\n'

        string += dumps_list(self.content)

        string += r'\end{tabular}'

        return string
