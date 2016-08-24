# -*- coding: utf-8 -*-
"""
This module implements several classes that represent basic latex commands.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import CommandBase, Environment, ContainerCommand
from .package import Package


class BasicCommand(CommandBase):
    """A command which takes no arguments or options."""

    def __init__(self):
        super().__init__()


class NewPage(BasicCommand):
    """A command that adds a new page to the document."""


class LineBreak(BasicCommand):
    """A command that adds a line break to the document."""


class NewLine(BasicCommand):
    """A command that adds a new line to the document."""


class HFill(BasicCommand):
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
    """An environment which makes the text size 'large'."""

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


class TextColor(ContainerCommand):
    """An environment which changes the text color of the data."""

    _repr_attributes_mapping = {
        "color": "arguments"
    }

    packages = [Package("xcolor")]

    def __init__(self, color, data):
        """
        Args
        ----
        color: str
            The color to set for the data inside of the environment.
        data: str or `~.LatexObject`
            The string or LatexObject to be formatted.
        """

        super().__init__(arguments=color, data=data)
