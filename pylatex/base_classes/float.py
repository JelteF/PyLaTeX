# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with floating environments.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from . import Environment, Command


class Float(Environment):

    """A class that represents a floating environment.

    :param data:
    :param position:

    :type data: list
    :type position: str
    :param data:
    :param position:
    :param seperate_paragraph:

    :type data: list
    :type position: str
    :type seperate_paragraph: bool
    """

    def __init__(self, data=None, position=None, seperate_paragraph=True,
                 **kwargs):

        super().__init__(data=data, options=position,
                         seperate_paragraph=seperate_paragraph, **kwargs)

    def add_caption(self, caption):
        """Add a caption to the float.

        :param caption:
        :type caption: str
        """

        self.append(Command('caption', caption))
