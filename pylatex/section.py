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

    #: Number the sections when the section element is compatible,
    #: by changing the `~.Section` class default all
    #: subclasses will also have the new default.
    numbering = True

    def __init__(self, title, numbering=None, **kwargs):
        """
        Args
        ----
        title: str
            The section title.
        numbering: bool
            Add a number before the section title.
        """

        self.title = title

        if numbering is not None:
            self.numbering = numbering

        super().__init__(**kwargs)

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
        string += '%\n' + self.dumps_content()

        return string


class Part(Section):
    """A class that represents a part."""


class Chapter(Section):
    """A class that represents a chapter."""


class Subsection(Section):
    """A class that represents a subsection."""


class Subsubsection(Section):
    """A class that represents a subsubsection."""


class Paragraph(Section):
    """A class that represents a paragraph."""


class Subparagraph(Section):
    """A class that represents a subparagraph."""
