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


class BaseLaTeXClass:

    """A class that has some basic functions for LaTeX functions."""

    def dumps(self):
        """Represents the class as a string in LaTeX syntax."""
        return ''

    def dump(self, file_, protocol=None):
        """Writes the LaTeX representation of the class to a file."""
        file_.write(self.dumps())

class BaseLaTeXContainer(BaseLaTeXClass, UserList):

    """A base class that can cointain other LaTeX content."""

    def __init__(self, data=None):
        if data is None:
            data = []

        self.data = data
