# -*- coding: utf-8 -*-
"""
    pylatex.lists
    ~~~~~~~

    This module implements the class that deals with latex List objects
    specifically Enumerate and Itemize.

    :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from .base_classes import BaseLaTeXNamedContainer


class List(BaseLaTeXNamedContainer):

    """A class that represents a list."""

    def __init__(self, list_spec=None, data=None, pos=None,
                 list_type="enumerate", **kwargs):
        """
            :param list_spec:
            :param list_type:
            :param data:
            :param pos:

            :type list_spec: str
            :type list_type: str
            :type data: list
            :type pos: list
        """
        super().__init__(list_type, data=data, options=pos,
                         argument=list_spec, **kwargs)

    def _item(self, label=None):
        """ Begin an item block. """
        if label:
            return r'\item[' + label + '] '

        return r'\item '

    def add_item(self, s):
        """ Adds an item to the list.

            :param s:

            :type s: string
        """
        self.append(self._item())
        self.append(s)


class Enumerate(List):

    """ A class that represents an enumerate list """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, list_type='enumerate', **kwargs)


class Itemize(List):

    """ A class that represents an itemize list """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, list_type='itemize', **kwargs)


class Description(List):

    """ A class that represents a description list """

    def __init__(self, *args, **kwargs):
        super(Description, self).__init__(*args, list_type='description',
                                          **kwargs)

    def add_item(self, label, s):
        """ Adds an item to the list.

            :param label:
            :param s:

            :type label: string
            :type s: string
        """
        self.append(self._item(label))
        self.append(s)
