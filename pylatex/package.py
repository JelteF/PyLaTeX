# -*- coding: utf-8 -*-
"""
This module implements the class that deals with packages.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import Command


class Package(Command):

    """A class that represents a package."""

    def __init__(self, name, options=None):
        """.

        Args
        ----
        name: str
            Name of the package.
        options: `str`, `list` or `~.Options`
            Options of the package.

        """

        super().__init__('usepackage', arguments=name, options=options)
