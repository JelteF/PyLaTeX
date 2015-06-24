# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with LaTeX lists.

These lists are specifically enumerate, itemize and description.

..  :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from .base_classes import Environment


class List(Environment):

    """A class that represents a list.

    :param list_spec:
    :param list_type:
    :param data:
    :param pos:

    :type list_spec: str
    :type list_type: str
    :type data: list
    :type pos: list
    """

    def __init__(self, list_spec=None, data=None, pos=None, **kwargs):
        super().__init__(data=data, options=pos, arguments=list_spec, **kwargs)

    def _item(self, label=None):
        """Begin an item block."""
        if label:
            return r'\item[' + label + '] '

        return r'\item '

    def add_item(self, s):
        """Add an item to the list.

        :param s:

        :type s: string
        """
        self.append(self._item())
        self.append(s)


class Enumerate(List):

    """A class that represents an enumerate list."""


class Itemize(List):

    """A class that represents an itemize list."""


class Description(List):

    """A class that represents a description list."""

    def add_item(self, label, s):
        """Add an item to the list.

        :param label:
        :param s:

        :type label: string
        :type s: string
        """
        self.append(self._item(label))
        self.append(s)
