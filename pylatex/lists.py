# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with LaTeX lists.

These lists are specifically enumerate, itemize and description.

..  :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from .base_classes import Environment, Command


class List(Environment):
    """A base class that represents a list."""

    def add_item(self, s):
        """Add an item to the list.

        Args
        ----
        s: str or `~.LatexObject`
            The item itself.
        """
        self.append(Command('item'))
        self.append(s)


class Enumerate(List):
    """A class that represents an enumerate list."""


class Itemize(List):
    """A class that represents an itemize list."""


class Description(List):
    """A class that represents a description list."""

    def add_item(self, label, s):
        """Add an item to the list.

        Args
        ----
        label: str
            Description of the item.
        s: str or `~.LatexObject`
            The item itself.
        """
        self.append(Command('item', options=label))
        self.append(s)
