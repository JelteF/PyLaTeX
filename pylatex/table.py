# -*- coding: utf-8 -*-
"""
This module implements the class that deals with tables.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import LatexObject, Container, Command, UnsafeCommand, \
    Float, Environment
from .package import Package
from .errors import TableRowSizeError
from .utils import dumps_list, NoEscape, escape_latex

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


class Tabular(Environment):
    """A class that represents a tabular."""

    _repr_attributes_mapping = {
        'table_spec': 'arguments',
        'pos': 'options',
    }

    def __init__(self, table_spec, data=None, pos=None, **kwargs):
        """
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

            if self.escape:
                start = escape_latex(start)
                end = escape_latex(end)

            self.append(UnsafeCommand('cline', start + '-' + end))

    def add_empty_row(self):
        """Add an empty row to the table."""

        self.append(NoEscape((self.width - 1) * '&' + r'\\'))

    def add_row(self, cells, *, escape=None, mapper=None, strict=True):
        """Add a row of cells to the table.

        Args
        ----
        cells: iterable, such as a `list` or `tuple`
            Each element of the iterable will become a the content of a cell.
        mapper: callable
            A function that should be called on all entries of the list after
            converting them to a string, for instance bold
        strict: bool
            Check for correct count of cells in row or not.
        """

        if escape is None:
            escape = self.escape

        # Propagate packages used in cells
        for c in cells:
            if isinstance(c, LatexObject):
                for p in c.packages:
                    self.packages.add(p)

        # Count cell contents
        cell_count = 0

        for c in cells:
            if isinstance(c, MultiColumn):
                cell_count += c.size
            else:
                cell_count += 1

        if strict and cell_count != self.width:
            msg = "Number of cells added to table ({}) " \
                "did not match table width ({})".format(cell_count, self.width)
            raise TableRowSizeError(msg)

        self.append(dumps_list(cells, escape=escape, token='&',
                               mapper=mapper) + NoEscape(r'\\'))


class MultiColumn(Container):
    """A class that represents a multicolumn inside of a table."""

    # TODO: Make this subclass CommandBase and Container

    def __init__(self, size, *, align='c', data=None):
        """
        Args
        ----
        size: int
            The amount of columns that this cell should fill.
        align: str
            How to align the content of the cell.
        data: str, list or `~.LatexObject`
            The content of the cell.
        """

        self.size = size
        self.align = align

        super().__init__(data=data)

    def dumps(self):
        """Represent the multicolumn as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        args = [self.size, self.align, self.dumps_content()]
        string = Command(self.latex_name, args).dumps()

        return string


class MultiRow(Container):
    """A class that represents a multirow in a table."""

    # TODO: Make this subclass CommandBase and Container

    packages = [Package('multirow')]

    def __init__(self, size, *, width='*', data=None):
        """
        Args
        ----
        size: int
            The amount of rows that this cell should fill.
        width: str
            Width of the cell. The default is ``*``, which means the content's
            natural width.
        data: str, list or `~.LatexObject`
            The content of the cell.
        """

        self.size = size
        self.width = width

        super().__init__(data=data)

    def dumps(self):
        """Represent the multirow as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        args = [self.size, self.width, self.dumps_content()]
        string = Command(self.latex_name, args).dumps()

        return string


class Table(Float):
    """A class that represents a table float."""


class Tabu(Tabular):
    """A class that represents a tabu (more flexible table)."""

    packages = [Package('tabu')]


class LongTable(Tabular):
    """A class that represents a longtable (multipage table)."""

    packages = [Package('longtable')]


class LongTabu(LongTable, Tabu):
    """A class that represents a longtabu (more flexible multipage table)."""
