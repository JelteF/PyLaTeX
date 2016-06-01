# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with LaTeX lists.

These lists are specifically enumerate, itemize and description.

..  :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from .base_classes import Environment, Command, Options
from .package import Package


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
    packages = [ Package('enumerate') ]
    
    def __init__(self, options=None, arguments=None, enumeration_symbol='1',
            **kwargs):
        r""" Initializes an enumerate environment
            
            Args
            ----
            options: str, list, Options
                Options to be added to the begin tag
            arguments: str, list, Arguments
                Arguments to be added to the begin tag
            enumeration_symbol: str
                Enumeration symbol to use for the table (/alph, /Alph, /roman)

        """
        options = Options(enumeration_symbol)
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
