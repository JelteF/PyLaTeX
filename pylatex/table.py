# -*- coding: utf-8 -*-
"""
This module implements the class that deals with tables.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import Container, Command, TabularBase, Float
from .package import Package


class MultiColumn(Container):
    """A class that represents a multicolumn inside of a table."""

    # TODO: Make this subclass CommandBase and Container

    def __init__(self, size, align='c', data=None):
        """.

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

        super().__init__(data)

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

    def __init__(self, size, width='*', data=None):
        """.

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

        super().__init__(data)

    def dumps(self):
        """Represent the multirow as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        args = [self.size, self.width, self.dumps_content()]
        string = Command(self.latex_name, args).dumps()

        return string


class Tabular(TabularBase):
    """A class that represents a tabular."""


class Table(Float):
    """A class that represents a table float."""


class Tabu(TabularBase):
    """A class that represents a tabu (more flexible table)."""

    packages = [Package('tabu')]


class LongTable(TabularBase):
    """A class that represents a longtable (multipage table)."""

    packages = [Package('longtable')]


class LongTabu(LongTable, Tabu):
    """A class that represents a longtabu (more flexible multipage table)."""
