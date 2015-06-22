# -*- coding: utf-8 -*-
"""
    pylatex.math
    ~~~~~~~~~~~~

    This module implements the class that deals with math.

    ..  :copyright: (c) 2014 by Jelte Fennema.
        :license: MIT, see License for more details.
"""

from .base_classes import BaseLaTeXContainer


class Math(BaseLaTeXContainer):
    def __init__(self, data=None, inline=False):
        """
            :param data:
            :param inline:

            :type data: list
            :type inline: bool
        """

        self.inline = inline
        super().__init__(data)

    def dumps(self):
        """
            :rtype: str
        """

        if self.inline:
            string = '$' + super().dumps(token=' ') + '$'
        else:
            string = '$$' + super().dumps(token=' ') + '$$\n'

        super().dumps()

        return string
