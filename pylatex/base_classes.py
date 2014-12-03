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
from contextlib import contextmanager


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
        self._cur_obj = self #to implement create

        super().__init__(packages=packages)

    def dumps(self):
        """Represents the container as a string in LaTeX syntax."""
        self.propegate_packages()

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

    @contextmanager
    def create(self, object):
        """Add a latex object to current container, context-manager style"""
        prev_obj = self._cur_obj
        self._cur_obj = object # so we don't have to keep track of the current object
        yield object # allows with ... as to be used as well
        self._cur_obj = prev_obj
        self._cur_obj.append(object)



class BaseLaTeXNamedContainer(BaseLaTeXContainer):

    """A base class for containers with one of a basic begin end syntax"""

    def __init__(self, name, data=None, packages=None, options=None):
        self.name = name
        self.options = options

        super().__init__(data=data, packages=packages)

    def dumps(self):
        """Represents the named container as a string in LaTeX syntax."""
        string = r'\begin{' + self.name + '}\n'

        if self.options is not None:
            string += '[' + self.options + ']'

        string += dumps_list(self)

        string += r'\end{' + self.name + '}\n'

        super().dumps()

        return string
