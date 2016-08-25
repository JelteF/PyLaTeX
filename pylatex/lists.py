# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with LaTeX lists.

These lists are specifically enumerate, itemize and description.

..  :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from .base_classes import Environment, Command
from .package import Package
from pylatex.utils import NoEscape


class List(Environment):
    """A base class that represents a list."""

    #: List environments cause compile errors when they do not contain items.
    #: This is why they are ommited fully if they are empty.
    omit_if_empty = True

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

    _repr_attributes_mapping = {
        "enumeration_symbol": "options"
    }

    def __init__(self, options=None, arguments=None, *,
                 enumeration_symbol=None, **kwargs):
        r"""
        Args
        ----
        options: str, list or `~.Options`
            Options to be added to the begin tag
        arguments: str, list or `~.Arguments`
            Arguments to be added to the begin tag
        enumeration_symbol: str
            The enumeration symbol to use, see the `enumitem
            <https://www.ctan.org/pkg/enumitem>`_ documentation to see what
            can be used here.
        """

        packages = []
        if enumeration_symbol is not None:
            packages = [Package("enumitem")]
            options = [NoEscape(enumeration_symbol)]
        self.enumeration_symbol = enumeration_symbol

        self.packages |= packages

        super().__init__(options=options, arguments=arguments, **kwargs)


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
