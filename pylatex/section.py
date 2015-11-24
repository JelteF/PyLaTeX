# -*- coding: utf-8 -*-
"""
This module implements the section type classes.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from .base_classes import Container, Command


class Section(Container):
    """A class that represents a section."""

    #: A section should normally start in its own paragraph
    end_paragraph = True

    def __init__(self, title, *args, numbering=True, **kwargs):
        """.

        Args
        ----
        title: str
            The section title.
        numbering: bool
            Add a number before the section title.

        """

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

        string = Command(self.latex_name + num, self.title).dumps()
        string += '\n' + self.dumps_content()

        return string


class Subsection(Section):
    """A class that represents a subsection."""


class Subsubsection(Section):
    """A class that represents a subsubsection."""
