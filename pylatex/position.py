# -*- coding: utf-8 -*-

from .base_classes import Environment, SpecialOptions
from .package import Package
from .utils import NoEscape


class Position(Environment):
    r"""Base class for positioning environments."""

    packages = [Package('ragged2e')]


class Center(Position):
    r"""Centered environment."""


class FlushLeft(Position):
    r"""Left-aligned environment."""


class FlushRight(Position):
    r"""Right-aligned environment."""


class MiniPage(Environment):
    r"""A class that allows the creation of minipages within document pages."""

    packages = [Package('ragged2e')]

    def __init__(self, *, width=NoEscape(r'\textwidth'),
                 height=None, adjustment='t', data=None, align='l'):
        r"""
        Args
        ----
        width: str
            width of the minipage
        height: str
            height of the minipage
        adjustment: str
            vertical allignment of text inside the minipage
        align: str
            alignment of the minibox
        """

        if height is not None:
            options = SpecialOptions(adjustment, NoEscape(height))
        else:
            options = adjustment

        arguments = [NoEscape(str(width))]

        super().__init__(arguments=arguments, options=options, data=data)

        if align == "l":
            self.append(NoEscape(r"\flushleft"))
        elif align == "c":
            self.append(NoEscape(r"\centering"))
        elif align == "r":
            self.append(NoEscape(r"\flushright"))


class TextBlock(Environment):
    r"""A class that represents a textblock environment.

    Make sure to set lengths of TPHorizModule and TPVertModule
    """

    _repr_attributes_mapping = {
        "width": "arguments"
    }

    packages = [Package('textpos')]

    def __init__(self, width, horizontal_pos, vertical_pos, *,
                 indent=False, data=None):
        r"""
        Args
        ----
        width: float
            Width of the text block in the units specified by TPHorizModule
        horizontal_pos: float
            Horizontal position in units specified by the TPHorizModule
        indent: bool
            Determines whether the text block has an indent before it
        vertical_pos: float
            Vertical position in units specified by the TPVertModule
        """

        arguments = width
        self.horizontal_pos = horizontal_pos
        self.vertical_pos = vertical_pos

        super().__init__(arguments=arguments)

        self.append("(%s, %s)" % (str(self.horizontal_pos),
                    str(self.vertical_pos)))

        if not indent:
            self.append(NoEscape(r'\noindent'))
