# -*- coding: utf-8 -*-
"""
    pylatex.varia
    ~~~~~~~

    This module implements the class that lets you insert custom Latex code at
    the beginning of the document. E.g. specifications on the paper geometry

    
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import BaseLaTeXContainer
from .package import Package

from collections import Counter
import re
import pdb


class Varia(BaseLaTeXContainer):

    """A class that represents a Graphic."""

    def __init__(self, code, data=None, packages=None):
        self.code = code
        super().__init__(data=data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        string = self.code
        super().dumps()
        return string
        


