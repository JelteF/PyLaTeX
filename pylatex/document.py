# -*- coding: utf-8 -*-
"""
    pylatex.document
    ~~~~~~~

    This module implements the class that deals with the full document.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
import subprocess
from .package import Package
from .command import Command
from .utils import dumps_list
from .base_classes import BaseLaTeXContainer


class Document(BaseLaTeXContainer):

    """
    A class that contains a full latex document. If needed, you can append
    stuff to the preamble or the packages if needed.
    """

    def __init__(self, filename='default_filename', documentclass='article',
                 fontenc='T1', inputenc='utf8', author=None, title=None,
                 date=None, data=None):
        self.filename = filename

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command('documentclass',
                                         arguments=documentclass)

        fontenc = Package('fontenc', options=fontenc)
        inputenc = Package('inputenc', options=inputenc)
        lmodern = Package('lmodern')
        packages = [fontenc, inputenc, lmodern]

        self.preamble = []

        if title is not None:
            self.preamble.append(Command('title', title))
        if author is not None:
            self.preamble.append(Command('author', author))
        if date is not None:
            self.preamble.append(Command('date', date))

        super().__init__(data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        document = r'\begin{document}' + os.linesep

        document += super().dumps() + os.linesep

        document += r'\end{document}' + os.linesep

        head = self.documentclass.dumps() + os.linesep
        head += self.dumps_packages() + os.linesep
        head += dumps_list(self.preamble) + os.linesep

        return head + os.linesep + document

    def generate_tex(self):
        """Generates a .tex file."""
        with open(self.filename + '.tex', 'w') as newf:
            self.dump(newf)

    def generate_pdf(self, clean=True):
        """Generates a pdf"""
        self.generate_tex()

        command = 'pdflatex --jobname="' + self.filename + '" "' + \
            self.filename + '.tex"'

        subprocess.check_call(command, shell=True)

        if clean:
            subprocess.call('rm "' + self.filename + '.aux" "' +
                            self.filename + '.log" "' +
                            self.filename + '.tex"', shell=True)
