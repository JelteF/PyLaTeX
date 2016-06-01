# -*- coding: utf-8 -*-

import os
import subprocess
import errno
from .base_classes import Environment, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir, NoEscape

class Header(Command):

    def __init__(self, lhead=None, chead=None, rhead=None, lfoot=None,
            cfoot=None, rfoot=None, header_thickness=0,
            footer_thickness=0):

        self._latex_name = "fancyhf"

        packages = [Package("fancyhdr")]

        self.lhead = self.set_lhead(lhead)
        self.chead = self.set_chead(chead)
        self.rhead = self.set_rhead(rhead)
        self.lfoot = self.set_lfoot(lfoot)
        self.cfoot = self.set_cfoot(cfoot)
        self.rfoot = self.set_rfoot(rfoot)
        self.header_thickness = str(header_thickness) + 'pt'
        self.footer_thickness = str(footer_thickness) + 'pt'

        super().__init__(command=self._latex_name, packages=packages)

    def dumps(self):
        head = super().dumps() + '{}\n'
        
        head += Command("pagestyle", arguments="fancy").dumps() + '\n'
        
        head += Command("renewcommand", arguments=[NoEscape(r'\headrulewidth'), self.header_thickness]).dumps() + '\n'

        head += Command("renewcommand", arguments=[NoEscape(r'\footrulewidth'), self.footer_thickness]).dumps() + '\n'

        if self.lhead is not None:
            head += Command("lhead",arguments=NoEscape(self.lhead)).dumps() + '\n'
        if self.chead is not None:
            head += Command("chead",arguments=NoEscape(self.chead)).dumps() + '\n'
        if self.rhead is not None:
            head += Command("rhead",arguments=NoEscape(self.rhead)).dumps() + '\n'
        if self.lfoot is not None:
            head += Command("lfoot",arguments=NoEscape(self.lfoot)).dumps() + '\n'
        if self.cfoot is not None:
            head += Command("cfoot",arguments=NoEscape(self.cfoot)).dumps() + '\n'
        if self.rfoot is not None:
            head += Command("rfoot",arguments=NoEscape(self.rfoot)).dumps() + '\n'

        return head


    def set_lhead(self, lhead):
        if lhead is not None:
            self.lhead = lhead.replace('\n', r'\linebreak')


    def set_chead(self, chead):
        if chead is not None:
            self.chead = chead.replace('\n', r'\linebreak')


    def set_rhead(self, rhead):
        if rhead is not None:
            self.rhead = rhead.replace('\n', r'\linebreak')


    def set_lfoot(self, lfoot):
        if lfoot is not None:
            self.lfoot = lfoot.replace('\n', r'\linebreak')


    def set_cfoot(self, cfoot):
        if cfoot is not None:
            self.cfoot = cfoot.replace('\n', r'\linebreak')


    def set_rfoot(self, rfoot):
        if rfoot is not None:
            self.rfoot = rfoot.replace('\n', r'\linebreak')

    def set_header_thickness(self, thickness):
        self.header_thickness = str(thickness) + 'pt'

    def set_footer_thickness(self, thickness):
        self.footer_thickness = str(thickness) + 'pt'
