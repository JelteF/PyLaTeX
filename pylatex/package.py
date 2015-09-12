# -*- coding: utf-8 -*-
'''
This module implements the class that deals with packages.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
'''

from .base_classes import Command


class Package(Command):

    '''A class that represents a package.

    :param name:
    :param base:
    :param options:

    :type name: str
    :type base: str
    :type options: str
    '''

    # TODO: Fix multiple types in this case for options:
    # str or list or `~.Options` instance

    def __init__(self, name, base='usepackage', options=None):
        super().__init__(base, arguments=name, options=options)
