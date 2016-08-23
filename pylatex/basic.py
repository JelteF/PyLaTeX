# -*- coding: utf-8 -*-
"""
This module implements several classes that represent basic latex commands.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import CommandBase, Environment


class Basic(CommandBase):
    """A command which takes no arguments or options."""

    def __init__(self):
        super().__init__()


class NewPage(Basic):
    """A command that adds a new page to the document."""


class LineBreak(Basic):
    """A command that adds a line break to the document."""


class NewLine(Basic):
    """A command that adds a new line to the document."""


class HFill(Basic):
    """A command that fills the current line in the document."""


class FontSize(Environment):
    """An environment which changes the font size."""

    _repr_attributes_mapping = {
        "size": "options"
    }

    def __init__(self, size, data):
        """
        Args
        ----
        size : str
            The name of the font size
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        self._latex_name = size
        super().__init__(data=data)


class HugeText(FontSize):
    """An environment which makes the text size 'Huge'."""

    def __init__(self, data):
        """
        Args
        ----
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(size="Huge", data=data)


class LargeText(FontSize):
    """An environment which makes the text size 'Large'."""

    def __init__(self, data):
        """
        Args
        ----
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(size="Large", data=data)


class MediumText(FontSize):
    """An environment which makes the text size 'Large'."""

    def __init__(self, data):
        """
        Args
        ----
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(size="large", data=data)


class SmallText(FontSize):
    """An environment which makes the text size 'small'."""

    def __init__(self, data):
        """
        Args
        ----
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(size="small", data=data)


class FootnoteText(FontSize):
    """An environment which makes the text size 'footnotesize'."""

    def __init__(self, data):
        """
        Args
        ----
        data : str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(size="footnotesize", data=data)
