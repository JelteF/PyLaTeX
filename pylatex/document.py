# -*- coding: utf-8 -*-
"""
    pylatex.document
    ~~~~~~~

    This module implements the class that deals with the full document.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import subprocess
from .package import Package
from .utils import dumps_list
from .base_classes import BaseLaTeXContainer
from collections import UserList


class Document(BaseLaTeXContainer):

    """A class that contains a full latex document."""

    def __init__(self, filename='default_filename', documentclass='article',
                 fontenc='T1', inputenc='utf8', author=None, title=None,
                 date=None, data=None):
        self.filename = filename

        self.documentclass = documentclass

        fontenc = Package('fontenc', fontenc)
        inputenc = Package('inputenc', inputenc)
        self.packages = [fontenc, inputenc, Package('lmodern'),
                         Package('amsmath')]

        self.author = author
        self.title = title
        self.date = date

        super().__init__(data)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        string = r'\documentclass{' + self.documentclass + '}'

        string += dumps_list(self.packages)

        if self.title is not None:
            string += r'\title{' + self.title + '}\n'
        if self.author is not None:
            string += r'\author{' + self.author + '}\n'
        if self.author is not None:
            string += r'\date{' + self.date + '}\n'

        string += r'\begin{document}'

        string += dumps_list(self)

        string += r'\end{document}'

        return string

    def generate_tex(self):
        """Generates a .tex file."""
        newf = open(self.filename + '.tex', 'w')
        self.dump(newf)
        newf.close()

    def generate_pdf(self, clean=True):
        """Generates a pdf"""
        self.generate_tex()

        command = 'pdflatex --jobname="' + self.filename + '" "' + \
            self.filename + '.tex"'

        subprocess.call(command, shell=True)

        if clean:
            subprocess.call('rm "' + self.filename + '.aux" "' +
                            self.filename + '.log" "' +
                            self.filename + '.tex"', shell=True)
