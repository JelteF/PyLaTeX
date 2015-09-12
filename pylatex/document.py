# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
import subprocess
import errno
from .base_classes import Container, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir


class Document(Container):

    r"""
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages.

    Args
    ----
    default_filepath: str
        The default path to save files.
    documentclass: str or `~.Command`
        The LaTeX class of the document.
    fontenc: str
        The option for the fontenc package.
    inputenc: str
        The option for the inputenc package.
    author: str
        The author of the document.
    title: str
        The title of the document.
    date: str
        The date of the document.
    maketitle: bool
        Whether ``\maketitle`` command is activated or not.
    data: list
        Initial content of the document.
    """

    def __init__(self, default_filepath='default_filepath',
                 documentclass='article', fontenc='T1', inputenc='utf8',
                 author='', title='', date='', maketitle=False, data=None):

        self.default_filepath = default_filepath
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
        """Represent the document as a string in LaTeX syntax.

        Returns
        -------
        str
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

    def generate_tex(self, filepath=''):
        """Generate a .tex file for the document.

        Args
        ----
        filepath: str
            The name of the file (without .tex), if this is not supplied the
            default filepath attribute is used as the path.
        """

        # TODO: Use None as the default for filepath instead of ''
        super().generate_tex(self.select_filepath(filepath))

    def generate_pdf(self, filepath='', clean=True, compiler='pdflatex',
                     silent=True):
        """Generate a pdf file from the document.

        Args
        ----
        filepath: str
            The name of the file (without .pdf)
        clean: bool
            Whether non-pdf files created by ``pdflatex`` must be removed
        silent: bool
            Whether to hide compiler output
        """

        filepath = self.select_filepath(filepath)
        filepath = os.path.join('.', filepath)

        cur_dir = os.getcwd()
        dest_dir = os.path.dirname(filepath)
        basename = os.path.basename(filepath)

        if basename == '':
            basename = 'default_basename'

        os.chdir(dest_dir)

        self.generate_tex(basename)

        command = [compiler, '--interaction', 'nonstopmode',
                   '--jobname', basename, basename + '.tex']

        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            print(e.output.decode())
            raise e
        else:
            if not silent:
                print(output.decode())

        if clean:
            for ext in ['aux', 'log', 'out', 'tex']:
                try:
                    os.remove(basename + '.' + ext)
                except (OSError, IOError) as e:
                    # Use FileNotFoundError when python 2 is dropped
                    if e.errno != errno.ENOENT:
                        raise

            rm_temp_dir()
        os.chdir(cur_dir)

    def select_filepath(self, filepath):
        """Make a choice between ``filepath`` and ``self.default_filepath``.

        Args
        ----
        filepath: str
            the filepath to be compared with ``self.default_filepath``

        Returns
        -------
        str
            The selected filepath
        """

        # TODO: Make this method private

        if filepath == '':
            return self.default_filepath
        else:
            if os.path.basename(filepath) == '':
                filepath = os.path.join(filepath, os.path.basename(
                    self.default_filepath))
            return filepath
