# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
import subprocess
import errno
from .base_classes import Environment, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir


class Document(Environment):

    r"""
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages.
    For instance, if you need to use ``\maketitle`` you can add the title,
    author and date commands to the preamble to make it work.

    """

    def __init__(self, default_filepath='default_filepath',
                 documentclass='article', fontenc='T1', inputenc='utf8',
                 lmodern=True, data=None):
        r""".

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
        lmodern: bool
            Use the Latin Modern font. This is a font that contains more glyphs
            than the standard LaTeX font.
        data: list
            Initial content of the document.
        """

        self.default_filepath = default_filepath

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command('documentclass',
                                         arguments=documentclass)

        fontenc = Package('fontenc', options=fontenc)
        inputenc = Package('inputenc', options=inputenc)
        if lmodern:
            lmodern = Package('lmodern')
        packages = [fontenc, inputenc, lmodern]

        self.preamble = []

        super().__init__(data=data, packages=packages)

    def dumps(self):
        """Represent the document as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        head = self.documentclass.dumps() + '\n'
        head += self.dumps_packages() + '\n'
        head += dumps_list(self.preamble) + '\n'

        return head + '\n' + super().dumps()

    def generate_tex(self, filepath=''):
        """Generate a .tex file for the document.

        Args
        ----
        filepath: str
            The name of the file (without .tex), if this is not supplied the
            default filepath attribute is used as the path.
        """

        # TODO: Use None as the default for filepath instead of ''
        super().generate_tex(self._select_filepath(filepath))

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

        filepath = self._select_filepath(filepath)
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

    def _select_filepath(self, filepath):
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

        if filepath == '':
            return self.default_filepath
        else:
            if os.path.basename(filepath) == '':
                filepath = os.path.join(filepath, os.path.basename(
                    self.default_filepath))
            return filepath
