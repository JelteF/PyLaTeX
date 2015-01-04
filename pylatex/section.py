# -*- coding: utf-8 -*-
"""
    pylatex.section
    ~~~~~~~

    This module implements the class that deals with sections.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import BaseLaTeXContainer
from .command import Command


class SectionBase(BaseLaTeXContainer):

    """A class that is the base for all section type classes"""

    def __init__(self, title, numbering=True, data=None):
        self.title = title
        self.numbering = numbering

        super().__init__(data)

    def dumps(self):
        """Represents the section as a string in LaTeX syntax."""

        if not self.numbering:
            num = '*'
        else:
            num = ''

        section_type = self.__class__.__name__.lower()
        string = Command(section_type + num, self.title).dumps()
        string += dumps_list(self)

        super().dumps()
        return string


class Section(SectionBase):

    """A class that represents a section."""


class Subsection(SectionBase):

    """A class that represents a subsection."""


class Subsubsection(SectionBase):

    """A class that represents a subsubsection."""
