# -*- coding: utf-8 -*-
"""
This module implements the class that deals with sections.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from . import Container, Command


class SectionBase(Container):

    """A class that is the base for all section type classes."""

    def __init__(self, title, numbering=True, *args, **kwargs):
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
        string += self.dumps_content()

        return string
