# -*- coding: utf-8 -*-

import os
import subprocess
import errno
from .base_classes import Container, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir, NoEscape, _latex_item_to_string

class HeaderCommand(Container):
    r""" Wrapper class for the header commands """

    omit_if_empty = False

    def __init__(self, name=None, options=None, data=None, **kwargs):
        r""" Initializes a header command
            
            Args
            ----
            name: str
                The name of the header command
            options: str, list or Options
                The options for the header command
            data: str or LatexObject
                The data to place inside the header command
        """

        self.arguments = name

        self.options = options

        super().__init__(data=data, **kwargs)

    def dumps(self):
        r""" Converts the command to a latex string """

        content = self.dumps_content()
        
        if not content.strip() and self.omit_if_empty:
            return ''
        
        string = ''

        start = Command(self.latex_name, arguments=self.arguments,
                options=self.options)

        string += start.dumps() + '{ \n'

        if content != '':
            string += content + '\n}'
        else:
            string += '}'

        return string


class PageStyle(HeaderCommand):
    r""" Allows the creation of new page styles """

    _latex_name = "fancypagestyle"

    packages = [ Package('fancyhdr') ]

    def __init__(self, name, data=None, header_thickness=0, footer_thickness=0):
        r""" 
            Args
            ----
            name: str
                The name of the page style
            header_thickness: float
                Value to set for the line under the header
            footer_thickness: float
                Value to set for the line over the footer
        """

        self.name = name

        super().__init__(data=data, name=self.name)

        self.change_thickness(element="header", thickness=header_thickness)
        self.change_thickness(element="footer", thickness=footer_thickness)

    def change_thickness(self, element, thickness):
        r""" Changes the thickness of the line under/over the header/footer
        to the specified thickness 
            
            Args
            ----
            element: str
                the name of the element to change thickness for: header, footer
            thickness: float
                the thickness to set the line to
        """
        
        if element == "header":
            self.data.append(Command("renewcommand", arguments =
                [NoEscape(r"\headrulewidth"), str(thickness) + 'pt']))
        elif element == "footer":
            self.data.append(Command("renewcommand", arguments =
                [NoEscape(r"\footrulewidth"), str(thickness) + 'pt']))

        

class Head(HeaderCommand):
    r""" Allows the creation of headers """

    _latex_name = "fancyhead"

    def __init__(self, position, data=None):
        r""" 
            Args
            ----
            position: str
                the headers position: L, C, R
        """

        self.position = position

        super().__init__(data=data, options = position)


class Foot(Head):
    r""" Allows the creation of footers"""

    _latex_name = "fancyfoot"
