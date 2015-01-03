# -*- coding: utf-8 -*-
"""
    pylatex.base_classes
    ~~~~~~~~~~~~~~~~~~~~

    This module implements base classes with inheritable functions for other
    LaTeX classes.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from collections import UserList
from ordered_set import OrderedSet
from pylatex.utils import dumps_list


class BaseLaTeXClass:

    """A class that has some basic functions for LaTeX functions."""

    def __init__(self, packages=None):
        if packages is None:
            packages = []

        self.packages = OrderedSet(packages)

    def dumps(self):
        """Represents the class as a string in LaTeX syntax."""

    def dump(self, file_):
        """Writes the LaTeX representation of the class to a file."""
        file_.write(self.dumps())

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax."""
        return dumps_list(self.packages)

    def dump_packages(self, file_):
        """Writes the LaTeX representation of the packages to a file."""
        file_.write(self.dumps_packages())


class BaseLaTeXContainer(BaseLaTeXClass, UserList):

    """A base class that can cointain other LaTeX content."""

    def __init__(self, data=None, packages=None):
        if data is None:
            data = []

        self.data = data

        super().__init__(packages=packages)

    def dumps(self, **kwargs):
        """Represents the container as a string in LaTeX syntax."""
        self.propegate_packages()
        return dumps_list(self, **kwargs)

    def propegate_packages(self):
        """Makes sure packages get propegated."""
        for item in self.data:
            if isinstance(item, BaseLaTeXClass):
                for p in item.packages:
                    self.packages.add(p)

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax."""
        self.propegate_packages()
        return dumps_list(self.packages)


class BaseLaTeXNamedContainer(BaseLaTeXContainer):

    """A base class for containers with one of a basic begin end syntax"""

    def __init__(self, name, options=None, argument=None, **kwargs):
        self.name = name
        self.options = options
        self.argument = argument

        super().__init__(**kwargs)

    def dumps(self):
        """Represents the named container as a string in LaTeX syntax."""
        string = r'\begin{' + self.name + '}'
        if self.options is not None:
            string += '[' + self.options + ']'
        if self.argument is not None:
            string += '{' + self.argument + '}'
        string += '\n'

        string += super().dumps()

        string += r'\end{' + self.name + '}'

        return string
