# -*- coding: utf-8 -*-
"""
This module implements the class that deals with packages.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import CommandBase


class Package(CommandBase):
    """A class that represents a package."""

    _latex_name = 'usepackage'

    _repr_attributes_mapping = {
        'name': 'arguments',
    }

    def __init__(self, name, options=None):
        """
        Args
        ----
        name: str
            Name of the package.
        options: `str`, `list` or `~.Options`
            Options of the package.

        """

        super().__init__(arguments=name, options=options)
    
    def is_package(self, name):
        """ Determines whether a package with the given name exists
            and if it does returns its index in the ordered set

            Args
            ----
            name: str
                Name of the package

            Returns
            -------
            int: index of the package or -1 if it does not exist

        """

        for package in self.packages:
            print(package)
