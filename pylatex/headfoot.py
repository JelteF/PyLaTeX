# -*- coding: utf-8 -*-

import os
import subprocess
import errno
from .base_classes import Environment, Command, CommandBase, PreambleCommand
from .package import Package
from .utils import dumps_list, rm_temp_dir, NoEscape, _latex_item_to_string

class FancyPageStyle(eCommand):

    packages = [ Package('fancyhdr') ]

    def __init__(self, name):
        self.name = name

        super().__init__()
        
    def append(self, element):
        r""" Appends the header/footer element to the page style """
        
        self.arguments.append(element)

class FancyHead(PreambleCommand):

    def __init__(self, position, data=None):
        self.position = position

        super().__init__(options = position)

    def append(self, element):
        r""" Appends elements to the header """

        self.arguments.append(element)


class FancyFoot(PreambleCommand):

    def __init__(self, position, data=None):
        self.position = position

        super().__init__(options = position)

    def append(self, element):
        r""" Appends elements to the footer """

        self.arguments.append(element)
        
class Header(Command):
    r""" A class which describes the header that will be displayed at the top
        of every page of a document
    """

    def __init__(self, lhead=None, chead=None, rhead=None, header_thickness=0, 
            footer_exists=False):
        r""" Initializes the header and sets its attributes 
            
            Args
            ----
            lhead: str
                Left header
            chead: str
                Center header
            rhead: str
                Right header
            header_thickness: float
                Header underline thickness measured in pt
            footer_exists: bool
                Determines if a footer already exists in the current document
        """

        self._latex_name = "fancyhf"

        self.footer_exists = footer_exists

        if not footer_exists:
            packages = [Package("fancyhdr")]
        else:
            packages = []

        self.set_params("lhead", lhead)
        self.set_params("chead", chead)
        self.set_params("rhead", rhead)
        self.set_header_thickness(header_thickness)
        
        super().__init__(command=self._latex_name, packages=packages)

    def dumps(self):
        r""" Converts the header to a Latex string
            
            Returns
            -------
            str
                the value of the Latex string
        """
        
        if not self.footer_exists:
            head = super().dumps() + '{}\n'
            head += Command("pagestyle", arguments="fancy").dumps() + '\n'
        else:
            head = ""

        head += self.header_thickness.dumps() + '\n'

        if self.lhead is not None:
            head += self.lhead.dumps() + '\n'
        if self.chead is not None:
            head += self.chead.dumps() + '\n'
        if self.rhead is not None:
            head += self.rhead.dumps() + '\n'

        return head


    def set_params(self, field, value):
        r""" Sets the parameter with the given field name to the given value

            Args
            ----
            field: str
                The name of the field being set
                Possible values: chead, lhead, rhead
            value: str
                The value the field is being set to
        """

        if (field == 'chead') or (field == 'lhead') or (field == 'rhead'):
            if value is not None:
                value = _latex_item_to_string(value)
                setattr(self, field, Command(field, arguments=NoEscape(value)))
            else:
                setattr(self, field, None)


    def set_header_thickness(self, thickness):
        r""" Sets the thickness of the line under the header

            Args
            ----
            thickness: float
                Value to set for the header thickness in pt
        """

        self.header_thickness = Command("renewcommand", arguments =
                [NoEscape(r'\headrulewidth'), str(thickness) + 'pt'])
        

    def recalculate_height(self, input_string):
        r""" Calculate header height based on the input string

        """

    def get_header_height(self):
        return self.header_height


class Footer(Command):

    def __init__(self, lfoot=None, cfoot=None, rfoot=None, footer_thickness=0,
            header_exists=False):
        r""" Initializes the footer and sets its attributes 
            
            Args
            ----
            lfoot: str
                Left footer
            cfoot: str
                Center footer
            rfoot: str
                Right footer
            footer_thickness: float
                Footer underline thickness measured in pt
            header_exists: bool
                Determines if a header exists in the current document
        """

        self._latex_name = "fancyhf"

        self.header_exists = header_exists
        
        if not header_exists:
            packages = [Package("fancyhdr")]
        else:
            packages = []

        self.set_params("lfoot", lfoot)
        self.set_params("cfoot", cfoot)
        self.set_params("rfoot", rfoot)
        self.set_footer_thickness(footer_thickness)

        super().__init__(command=self._latex_name, packages=packages)


    def set_params(self, field, value):
        r""" Sets the parameter with the given field name to the given value

            Args
            ----
            field: str
                The name of the field being set
                Possible values: cfoot, lfoot, rfoot
            value: str
                The value the field is being set to
        """

        if (field == 'cfoot') or (field == 'lfoot') or (field == 'rfoot'):
            if value is not None:
                value = _latex_item_to_string(value)
                setattr(self, field, Command(field, arguments=NoEscape(value)))
            else:
                setattr(self, field, None)


    def dumps(self):
        r""" Converts the footer to a Latex string

            Returns
            -------
            str
                the value of the Latex string
        """
        
        if not self.header_exists:
            head = super().dumps() + '{}\n'
            head += Command("pagestyle", arguments="fancy").dumps() + '\n'
        else:
            head = ""

        head += self.footer_thickness.dumps() + '\n'

        if self.lfoot is not None:
            head += self.lfoot.dumps()+ '\n'
        if self.cfoot is not None:
            head += self.cfoot.dumps() + '\n'
        if self.rfoot is not None:
            head += self.rfoot.dumps() + '\n'

        return head


    def set_footer_thickness(self, thickness):
        r""" Sets the thickness of the line over the footer

            Args
            ----
            thickness: float
                Value to set for the footer thickness in pt
        """

        self.footer_thickness = Command("renewcommand", arguments =
                [NoEscape(r'\footrulewidth'), str(thickness) + 'pt'])

