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
from .utils import dumps_list, rm_tmp
from .base_classes import BaseLaTeXContainer



class Document(BaseLaTeXContainer):

    """
    A class that contains a full LaTeX document. If needed, you can append
    stuff to the preamble or the packages.
    """

    def __init__(self, default_filename='default_filename',
                 documentclass='article', fontenc='T1', inputenc='utf8',
                 author='', title='', date='', data=None, maketitle=False):
        """
            :param default_filename: the default filename to save files
            :param documentclass: the LaTeX class of the document
            :param fontenc: the option for the fontenc package
            :param inputenc: the option for the inputenc package
            :param author: the author of the document
            :param title: the title of the document
            :param date: the date of the document
            :param data:
            :param maketitle: whether `\maketitle` command is activated or not.

            :type default_filename: str
            :type documentclass: str or :class:`command.Command` instance
            :type fontenc: str
            :type inputenc: str
            :type author: str
            :type title: str
            :type date: str
            :type data: list
            :type maketitle: bool
        """

        self.default_filename = default_filename
        self.maketitle = maketitle

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

        self.preamble.append(Command('title', title))
        self.preamble.append(Command('author', author))
        self.preamble.append(Command('date', date))

        super().__init__(data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax.

            :return:
            :rtype: str
        """

        document = r'\begin{document}' + os.linesep

        if self.maketitle:
            document += r'\maketitle' + os.linesep

        document += super().dumps() + os.linesep

        document += r'\end{document}' + os.linesep

        head = self.documentclass.dumps() + os.linesep
        head += self.dumps_packages() + os.linesep
        head += dumps_list(self.preamble) + os.linesep

        return head + os.linesep + document

    def generate_tex(self, filename=''):
        """Generates a .tex file.

            :param filename: the name of the file

            :type filename: str
        """

        filename = self.select_filename(filename)

        with open(filename + '.tex', 'w') as newf:
            self.dump(newf)

    def generate_pdf(self, filename='', clean=True):
        """Generates a .pdf file.

            :param filename: the name of the file
            :param clean: whether non-pdf files created by `pdflatex` must be
            removed or not

            :type filename: str
            :type clean: bool
        """

        filename = self.select_filename(filename)

        self.generate_tex(filename)

        command = 'pdflatex --jobname="' + filename + '" "' + filename + '.tex"'

        subprocess.check_call(command, shell=True)

        if clean:
            subprocess.call('rm "' + filename + '.aux"', shell=True)
            subprocess.call('rm "' + filename + '.log"', shell=True)
            subprocess.call('rm "' + filename + '.tex"', shell=True)
            subprocess.call('rm "' + filename + '.out"', shell=True)
        
        rm_tmp()
        
    def select_filename(self, filename):
        """Makes a choice between `filename` and `self.default_filename`.

            :param filename: the filename to be compared with
            `self.default_filename`

            :type filename: str

            :return: The selected filename
            :rtype: str
        """

        if filename == '':
            return self.default_filename
        else:
            return filename
