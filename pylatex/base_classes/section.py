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

    Args
    ----
    title: str
        The section title.
    numbering: bool
        Add a number before the section title.

    """

    def __init__(self, title, numbering=True, *args, **kwargs):
        self.title = title
        self.numbering = numbering

        super().__init__(*args, **kwargs)

    def dumps(self):
        """Represent the section as a string in LaTeX syntax.

        Returns
        -------
        str

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
