# -*- coding: utf-8 -*-
"""
This module implements the class that deals with tables.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import LatexObject, Container, Command, UnsafeCommand, \
    Float, Environment
from .package import Package
from .errors import TableRowSizeError, TableError
from .utils import dumps_list, NoEscape, escape_latex

from collections import Counter
import re


# The letters used to count the table width
COLUMN_LETTERS = ['l', 'c', 'r', 'p', 'm', 'b', 'X']


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

    # Remove things like {\bfseries}
    cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)

    # Remove X[] in tabu environments so they dont interfere with column count
    cleaner_spec = re.sub(r'X\[(.*?(.))\]', r'\2', cleaner_spec)
    spec_counter = Counter(cleaner_spec)

    return sum(spec_counter[l] for l in COLUMN_LETTERS)


class Tabular(Environment):
    """A class that represents a tabular."""

    _repr_attributes_mapping = {
        'table_spec': 'arguments',
        'pos': 'options',
    }

    def __init__(self, table_spec, data=None, pos=None, *,
                 row_height=None, col_space=None, width=None, arguments=None,
                 **kwargs):
        """
        Args
        ----
        table_spec: str
            A string that represents how many columns a table should have and
            if it should contain vertical lines and where.
        pos: list
        row_height: float
            Specifies the heights of the rows in relation to the default
            row height
        col_space: str
            Specifies the spacing between table columns
        arguments: str or `list`
            The arguments to append to the table
        width: int
            The amount of columns that the table has. If this is `None` it is
            calculated based on the ``table_spec``, but this is only works for
            simple specs. In cases where this calculation is wrong override the
            width using this argument.

        References
        ----------
        * https://en.wikibooks.org/wiki/LaTeX/Tables#The_tabular_environment
        """

        if width is None:
            self.width = _get_table_width(table_spec)
        else:
            self.width = width

        self.row_height = row_height
        self.col_space = col_space

        # Append the table_spec to the arguments list
        if arguments is not None:
            if isinstance(arguments, str):
                arguments = [arguments]
        else:
            arguments = []

        arguments.append(table_spec)

        super().__init__(data=data, options=pos,
                         arguments=arguments, **kwargs)

        # Parameter that determines if the xcolor package has been added.
        self.color = False

    def dumps(self):
        r"""Turn the Latex Object into a string in Latex format."""

        dump = ""

        if self.row_height is not None:
            row_height = Command('renewcommand', arguments=[
                NoEscape(r'\arraystretch'),
                self.row_height])
            dump += row_height.dumps() + '%\n'

        if self.col_space is not None:
            col_space = Command('setlength', arguments=[
                NoEscape(r'\tabcolsep'),
                self.col_space])
            dump += col_space.dumps() + '%\n'

        return dump + super().dumps()

    def add_hline(self, start=None, end=None, *, color=None):
        """Add a horizontal line to the table.

        Args
        ----
        start: int
            At what cell the line should begin
        end: int
            At what cell the line should end
        color: str
            The hline color.
        """

        if color is not None:
            if not self.color:
                self.packages.append(Package('xcolor', options='table'))
                self.color = True
            color_command = Command(command="arrayrulecolor", arguments=color)
            self.append(color_command)

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

    def add_row(self, cells, *, color=None, escape=None, mapper=None,
                strict=True):
        """Add a row of cells to the table.

        Args
        ----
        cells: iterable, such as a `list` or `tuple`
            Each element of the iterable will become a the content of a cell.
        color: str
            The name of the color used to highlight the row
        mapper: callable or `list`
            A function or a list of functions that should be called on all
            entries of the list after converting them to a string,
            for instance bold
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

        if color is not None:
            if not self.color:
                self.packages.append(Package("xcolor", options='table'))
                self.color = True
            color_command = Command(command="rowcolor", arguments=color)
            self.append(color_command)

        self.append(dumps_list(cells, escape=escape, token='&',
                    mapper=mapper) + NoEscape(r'\\'))


class Tabularx(Tabular):
    """A class that represents a tabularx environment."""

    packages = [Package('tabularx')]


class MultiColumn(Container):
    """A class that represents a multicolumn inside of a table."""

    # TODO: Make this subclass of CommandBase and Container

    def __init__(self, size, *, align='c', color=None, data=None):
        """
        Args
        ----
        size: int
            The amount of columns that this cell should fill.
        align: str
            How to align the content of the cell.
        data: str, list or `~.LatexObject`
            The content of the cell.
        color: str
            The color for the MultiColumn
        """

        self.size = size
        self.align = align

        super().__init__(data=data)

        # Add a cell color to the MultiColumn
        if color is not None:
            color_command = Command("cellcolor", arguments=color)
            self.append(color_command)

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

    def __init__(self, size, *, width='*', color=None, data=None):
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
        color: str
            The color for the MultiRow
        """

        self.size = size
        self.width = width

        super().__init__(data=data)

        if color is not None:
            color_command = Command("cellcolor", arguments=color)
            self.append(color_command)

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

    header = False

    def end_table_header(self):
        r"""End the table header which will appear on every page."""

        if self.header:
            msg = "Table already has a header"
            raise TableError(msg)

        self.header = True

        self.append(NoEscape(r'\endhead'))


class LongTabu(LongTable, Tabu):
    """A class that represents a longtabu (more flexible multipage table)."""


class Column(UnsafeCommand):
    """A class representing a new column type."""

    _repr_attributes_mapping = {
        'name': 'arguments',
        'base': 'arguments',
        'modifications': 'arguments',
        'parameters': 'options'
    }

    def __init__(self, name, base, modifications, parameters=None):
        """
        Args
        ----
        name: str
            The name of the new column type
        base: str
            The name of the base column type
        modifications: str
            The modifications made to the column type
        parameters: int
            The number of parameters inside the modifications
        """

        COLUMN_LETTERS.append(name)

        modified = r">{%s\arraybackslash}%s" % (modifications, base)

        super().__init__(command="newcolumntype", arguments=[name, modified],
                         options=parameters, extra_arguments=name)
