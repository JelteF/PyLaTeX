# -*- coding: utf-8 -*-
"""
This module implements the class that deals with math.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import Container


class Math(Container):

    """A class representing a math environment.

    :param data:
    :param inline:

    :type data: list
    :type inline: bool
    """

    def __init__(self, data=None, inline=False):
        self.inline = inline
        super().__init__(data)

    def dumps(self):
        """Return a LaTeX formatted string representing the object.

        :rtype: str
        """

        if self.inline:
            string = '$' + super().dumps(token=' ') + '$'
        else:
            string = '$$' + super().dumps(token=' ') + '$$\n'

        super().dumps()

        return string
