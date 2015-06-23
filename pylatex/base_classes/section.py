# -*- coding: utf-8 -*-
"""
This module implements the class that deals with sections.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from . import Container, Command
from ..utils import dumps_list


class SectionBase(Container):

    """A class that is the base for all section type classes.

    :param title:
    :param numbering:
    :param data:

    :type title: str
    :type numbering: bool
    :type data: list
    """

    def __init__(self, title, numbering=True, data=None):
        self.title = title
        self.numbering = numbering

        super().__init__(data)

    def dumps(self):
        """Represent the section as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        if not self.numbering:
            num = '*'
        else:
            num = ''

        section_type = self.__class__.__name__.lower()
        string = Command(section_type + num, self.title).dumps()
        string += dumps_list(self)

        super().dumps()

        return string
