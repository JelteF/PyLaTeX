# -*- coding: utf-8 -*-
"""
    pylatex.section
    ~~~~~~~

    This module implements the class that deals with sections.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list


class Section:

    """A class that represents a section."""

    def __init__(self, title, numbering=True):
        self.title = title
        self.numbering = numbering

        self.content = []

    def dumps(self):
        """Represents the section as a string in LaTeX syntax."""
        if self.numbering:
            num = '*'
        else:
            num = ''

        base = r'\section' + num + '{' + self.title + '}\n'
        return base + dumps_list(self.content)
