# -*- coding: utf-8 -*-
"""
    pylatex.package
    ~~~~~~~

    This module implements the class that deals with packages.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .command import Command


class Package(Command):

    """A class that represents a package."""

    def __init__(self, name, base='usepackage', options=None):
        super().__init__(base, arguments=name, options=options)
