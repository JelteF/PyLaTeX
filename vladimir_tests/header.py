# -*- coding: utf-8 -*-

import os
import subprocess
import errno
from .base_classes import Environment, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir

class Header(Command):

    def __init__(self, lhead=None, chead=None, rhead=None):
        self._latex_name = "fancyhf"

        packages = [Package("fancyhdr")]

        self.lhead = lhead
        self.chead = chead
        self.rhead = rhead
        
        super().__init__(command=self._latex_name, packages=packages)

    def dumps(self):
        head = super().dumps() + '\n'

        head += Command("lhead",arguments=self.lhead).dumps() + '\n'
        head += Command("chead",arguments=self.chead).dumps() + '\n'
        head += Command("rhead",arguments=self.rhead).dumps()

        return head



