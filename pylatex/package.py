# -*- coding: utf-8 -*-
"""
    pylatex.package
    ~~~~~~~

    This module implements the class that deals with packages.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


class Package:

    """A class that represents a package."""

    def __init__(self, name, option=None):
        self.name = name
        self.option = option

    def dumps(self):
        """Represents the package as a string in LaTeX syntax."""
        if self.option is None:
            option = ''
        else:
            option = '[' + self.option + ']'

        return r'\usepackage' + option + '{' + self.name + '}\n'
