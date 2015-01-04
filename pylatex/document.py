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
from .arguments import Arguments


class DocumentClass(BaseLaTeXContainer):
    """
    Represents the LaTex ``\documentclass`` command.
    ::
        >>> DocumentClass().dumps()
        '\documentclass{article}'
        >>> DocumentClass('report', Arguments('12pt', 'a4paper', 'twoside')).dumps()
        '\\documentclass[12pt,a4paper,twoside]{report}'
    """

    def __init__(self, class_name='article', options=None):
        """
        Creates a LaTex ``\documentclass`` command with the specified document class and options.

        :param class_name: The name of the LaTex document class to be used
        :type class_name: String
        :param options: The options to pass to the ``\documentclass`` command
        :type options: pylatex.arguments.Arguments
        """
        self.class_name = Arguments(class_name)
        if isinstance(options, Arguments):
            self.options = options
        else:
            self.options = Arguments()
        self.options.optional = True

    def dumps(self):
        return '\\documentclass{options}{classname}'.format(options=self.options.dumps(),
                                                            classname=self.class_name.dumps())


class Document(BaseLaTeXContainer):
    """A class that contains a full latex document."""

    def __init__(self, filename='default_filename', documentclass=None,
                 fontenc='T1', inputenc='utf8', author=None, title=None,
                 date=None, data=None):
        self.filename = filename

        if isinstance(documentclass, DocumentClass):
            self.documentclass = documentclass
        else:
            self.documentclass = DocumentClass()

        fontenc = Package('fontenc', option=fontenc)
        inputenc = Package('inputenc', option=inputenc)
        packages = [fontenc, inputenc, Package('lmodern')]

        if title is not None:
            packages.append(Package(title, base='title'))
        if author is not None:
            packages.append(Package(author, base='author'))
        if date is not None:
            packages.append(Package(date, base='date'))

        super().__init__(data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        document = r'\begin{document}'

        document += dumps_list(self)

        document += r'\end{document}'

        super().dumps()

        head = self.documentclass.dumps()

        head += self.dumps_packages()

        return head + document

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

        subprocess.check_call(command, shell=True)

        if clean:
            subprocess.call('rm "' + self.filename + '.aux" "' +
                            self.filename + '.log" "' +
                            self.filename + '.tex"', shell=True)
