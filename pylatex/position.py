# -*- coding: utf-8 -*-

from .base_classes import Environment, UnsafeCommand, SpecialOptions
from .package import Package
from .utils import NoEscape, line_break, escape_latex, fix_filename


class Position(Environment):
    r""" Base class for positioning environments
    """
    packages = [Package('ragged2e')]

class Center(Position):
    r""" Centered environment """


class Flushleft(Position):
    r""" Left-aligned environment """


class Flushright(Position):
    r""" Right-aligned environment """


class Minipage(Environment):
    r""" A class that allows the creation of minipages within document pages """
    
    def __init__(self, width=NoEscape(r'\textwidth'),
            height=NoEscape('\height'), adjustment='t'):
        r""" Instantiates a minipage within the current environment
	
            Args
            ----
            width: str
                width of the minipage
            height: str
                height of the minipage
            adjustment: str
                vertical allignment of text inside the minipage
        """

        options = SpecialOptions(adjustment, height)
        arguments = [ NoEscape(str(width)) ]

        super().__init__(arguments = arguments, options=options)

class TextBlock(Environment):

    def __init__(self, width, horizontal_pos, vertical_pos, absolute=False,
            data=None):
        r""" Initializes a text block environment

            Args
            ----
            width: float
                Width of the text block in the units specified by TPHorizModule
            horizontal_pos: float
                Horizontal position in units specified by the TPHorizModule
            absolute: bool
                Determines whether the item is positioned absolutelly
            vertical_pos: float
                Vertical position in units specified by the TPVertModule
        """

        arguments = width
        self.horizontal_pos = horizontal_pos
        self.vertical_pos = vertical_pos

        package_options = None

        if absolute:
            package_options = 'absolute'

        self.packages.append( Package('textpos', options=package_options))

        super().__init__(arguments=arguments)
