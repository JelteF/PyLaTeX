# -*- coding: utf-8 -*-

from .base_classes import Environment, Command, SpecialOptions
from .package import Package
from .utils import NoEscape, line_break, escape_latex, fix_filename, new_line, horizontal_skip, vertical_skip, text_box


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
            height=None, adjustment='t', data=None):
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
        if height is not None:
            options = SpecialOptions(adjustment, height)
        else:
            options = adjustment

        arguments = [ NoEscape(str(width)) ]

        super().__init__(arguments = arguments, options=options, data=data)

class TextBlock(Environment):
    r""" A class that represents a textblock environment.

        Make sure to set lengths of TPHorizModule and TPVertModule
    """

    def __init__(self, width, horizontal_pos, vertical_pos, absolute=False,
            indent=False, data=None):
        r""" Initializes a text block environment

            Args
            ----
            width: float
                Width of the text block in the units specified by TPHorizModule
            horizontal_pos: float
                Horizontal position in units specified by the TPHorizModule
            absolute: bool
                Determines whether the item is positioned absolutelly
            indent: bool
                Determines whether the text block has an indent before it
            vertical_pos: float
                Vertical position in units specified by the TPVertModule
        """

        arguments = width
        self.horizontal_pos = horizontal_pos
        self.vertical_pos = vertical_pos

        package_options = None

        if absolute:
            package_options = 'absolute'

        self.packages.append(Package('textpos', options=package_options))

        super().__init__(arguments=arguments)

        if indent == False:
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
 

class Fields(Minipage):
    r""" A class that defines an area of fields """

    _latex_name = "minipage"

    def __init__(self, page_width=21.66, margin=1.27, box_height=1.5, units="cm"):
        r""" 
            Args
            ----
            page_width: float
                the width of the page in units
            margin: float
                the height of the page in units
            box_height: float
                the height of the box in units
            units: str
                the units used
        """
        
        self.text_width = page_width - 2 * margin
        self.box_height = box_height
        self.units = units

        super().__init__()

    
    def add_box(self, box_width, data=None):
        r""" Add a box to the current line of boxes 
            
            Args
            ----
            box_width: float
                the width of the box in units
            data: str, LatexObject
                the data to be included inside the box

        """

        if box_width > self.text_width:
            print ("Error: box overflow, putting on next line")
            self.add_new_row()
        
        width = str(box_width) + self.units
        height = str(self.box_height) + self.units

        box = Minipage(width=width, height=height, data=data)

        self.append(text_box(box.dumps()))
        self.append(horizontal_skip("-7pt"))

    def get_text_width(self):
        r""" Returns the value that is left for the text width """

        return self.text_width

    def add_new_row(self):

        self.append(new_line())
