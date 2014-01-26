# -*- coding: utf-8 -*-
"""
    pylatex.package
    ~~~~~~~

    This module implements the class that deals with packages.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import BaseLaTeXClass


class Package:

    """A class that represents a package."""

    def __init__(self, name, base='usepackage', option=None):
        self.base = base
        self.name = name
        self.option = option

    def dumps(self):
        """Represents the package as a string in LaTeX syntax."""
        if self.option is None:
            option = ''
        else:
            option = '[' + self.option + ']'

        return '\\'+ self.base + option + '{' + self.name + '}\n'
