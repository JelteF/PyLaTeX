# -*- coding: utf-8 -*-

from .base_classes import Environment, Command, SpecialOptions, Arguments
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

    def __init__(self, width=NoEscape(r'\textwidth'),
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

    packages = [Package('textpos')]

    def __init__(self, width, horizontal_pos, vertical_pos,
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

        if not indent:
            self.append(NoEscape(r'\noindent'))

    def dumps(self):
        """Represent the environment as a string in LaTeX syntax.

        Returns
        -------
        str
            A LaTeX string representing the environment.
        """

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        string = ''

        # Something other than None needs to be used as extra arguments, that
        # way the options end up behind the latex_name argument.
        if self.arguments is None:
            extra_arguments = Arguments()
        else:
            extra_arguments = self.arguments

        begin = Command('begin', self.latex_name, self.options,
                        extra_arguments=extra_arguments)

        string += (begin.dumps() + '(' + str(self.horizontal_pos) + ',' +
                   str(self.vertical_pos) + ')' + '\n')

        string += content + '\n'

        string += Command('end', self.latex_name).dumps()

        return string
