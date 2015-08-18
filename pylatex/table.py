# -*- coding: utf-8 -*-
"""
This module implements the class that deals with tables.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import Container, Command, TabularBase
from .package import Package

from warnings import warn


class MultiColumn(Container):

    """A class that represents a multicolumn inside of a table.

    :param size:
    :param align:
    :param data:

    :type size: int
    :type align: str
    :type data: str

    TODO:
    type of data can also be list
    """

    def __init__(self, size, align='|c|', data=None):
        self.size = size
        self.align = align

        super().__init__(data)

    def dumps(self):
        """Represent the multicolumn as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        multicolumn_type = self.__class__.__name__.lower()
        args = [self.size, self.align, dumps_list(self.data)]
        string = Command(multicolumn_type, args).dumps()
        string += dumps_list(self)

        super().dumps()

        return string


class MultiRow(Container):

    """A class that represents a multirow in a table.

    :param size:
    :param width:
    :param data:

    :type size: int
    :type width: str
    :type data: str

    TODO:
    type of data can also be list
    """

    def __init__(self, size, width='*', data=None):
        self.size = size
        self.width = width

        packages = [Package('multirow')]
        super().__init__(data, packages=packages)

    def dumps(self):
        """Represent the multirow as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        multirow_type = self.__class__.__name__.lower()
        args = [self.size, self.width, dumps_list(self.data)]
        string = Command(multirow_type, args).dumps()
        string += dumps_list(self)

        super().dumps()

        return string


class Tabular(TabularBase):

    """A class that represents a tabular."""


class Table(Tabular):

    """A legacy name for the class that represents a tabular."""

    container_name = 'tabular'

    def __init__(self, *args, **kwargs):
        warn('Table is going te be deprecated in favor of Tabular',
             PendingDeprecationWarning)
        super().__init__(*args, **kwargs)


class Tabu(TabularBase):

    """A class that represents a tabu (more flexible table)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, packages=[Package('tabu')], **kwargs)


class LongTable(TabularBase):

    """A class that represents a longtable (multipage table)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, packages=[Package('longtable')], **kwargs)


class LongTabu(TabularBase):

    """A class that represents a longtabu (more flexible multipage table)."""

    def __init__(self, *args, **kwargs):
        packages = [Package('tabu'), Package('longtable')]

        super().__init__(*args, packages=packages, **kwargs)
