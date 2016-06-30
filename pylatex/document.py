# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
import subprocess
import errno
from .base_classes import Environment, Command, Container, LatexObject, \
    UnsafeCommand
from .package import Package
from .utils import dumps_list, rm_temp_dir


class Document(Environment):
    r"""
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages.
    For instance, if you need to use ``\maketitle`` you can add the title,
    author and date commands to the preamble to make it work.

    """

    def __init__(self, default_filepath='default_filepath', *,
                 documentclass='article', fontenc='T1', inputenc='utf8',
                 lmodern=True, textcomp=True, lscape=False, page_numbers=True,
                 margin='0.5in', header_height='12pt', indent=False,
                 header_sep='5pt', data=None, font_size="normalsize"):
        r"""
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
        textcomp: bool
            Adds even more glyphs, for instance the Euro (€) sign.
        lscape: bool
            Adds the ability to orientate the document in landscape mode
        header_height: str
            Controls the header height of the document
        header_sep: str
            Controls the sepparation between the header and the content
        page_numbers: bool
            Adds the ability to add page numbers to the document
        margin: str
            Modifies the default document margin
        indent: bool
            Determines whether or not the document requires indentation
        data: list
            Initial content of the document.
        font_size: str
            The font size to declare as normalsize
        """

        self.default_filepath = default_filepath

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command('documentclass',
                                         arguments=documentclass)

        # These variables are used by the __repr__ method
        self._fontenc = fontenc
        self._inputenc = inputenc
        self._lmodern = lmodern
        self._lscape = lscape
        self.header_height = header_height
        self.header_sep = header_sep

        fontenc = Package('fontenc', options=fontenc)
        inputenc = Package('inputenc', options=inputenc)
        geometry_options = ['includeheadfoot', 'margin=' + margin,
                            'headheight=' + header_height,
                            'headsep=' + header_sep]
        packages = [fontenc, inputenc]

        if lmodern:
            packages.append(Package('lmodern'))
        if textcomp:
            packages.append(Package('textcomp'))
        if lscape:
            geometry_options.append('landscape')
        if page_numbers:
            packages.append(Package('lastpage'))

        packages.append(Package('geometry', options=geometry_options))

        super().__init__(data=data)

        self.packages |= packages

        self.preamble = []

        if not page_numbers:
            self.change_document_style("empty")

        if not indent:
            self.change_length("\parindent", "0pt")

        # No colors have been added to the document yet
        self.color = False
        self.watermark = False

        self.append(Command(command=font_size))

    def _propagate_packages(self):
        r"""Propogate packages.

        Make sure that all the packages included in the previous containers
        are part of the full list of packages.
        """

        super()._propagate_packages()

        for item in (self.preamble):
            if isinstance(item, LatexObject):
                if isinstance(item, Container):
                    item._propagate_packages()
                for p in item.packages:
                    self.packages.add(p)

    def dumps(self):
        """Represent the document as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        head = self.documentclass.dumps() + '%\n'
        head += self.dumps_packages() + '%\n'
        head += dumps_list(self.preamble) + '%\n'

        return head + '%\n' + super().dumps()

    def generate_tex(self, filepath=None):
        """Generate a .tex file for the document.

        Args
        ----
        filepath: str
            The name of the file (without .tex), if this is not supplied the
            default filepath attribute is used as the path.
        """

        super().generate_tex(self._select_filepath(filepath))

    def generate_pdf(self, filepath=None, *, clean=True, clean_tex=True,
                     compiler=None, compiler_args=None, silent=True):
        """Generate a pdf file from the document.

        Args
        ----
        filepath: str
            The name of the file (without .pdf), if it is `None` the
            ``default_filepath`` attribute will be used.
        clean: bool
            Whether non-pdf files created that are created during compilation
            should be removed.
        clean_tex: bool
            Also remove the generated tex file.
        compiler: `str` or `None`
            The name of the LaTeX compiler to use. If it is None, PyLaTeX will
            choose a fitting one on its own. Starting with mklatex and then
            pdflatex.
        compiler_args: `list` or `None`
            Extra arguments that should be passed to the LaTeX compiler. If
            this is None it defaults to an empty list.
        silent: bool
            Whether to hide compiler output
        """

        if compiler_args is None:
            compiler_args = []

        filepath = self._select_filepath(filepath)
        filepath = os.path.join('.', filepath)

        cur_dir = os.getcwd()
        dest_dir = os.path.dirname(filepath)
        basename = os.path.basename(filepath)

        if basename == '':
            basename = 'default_basename'

        os.chdir(dest_dir)

        self.generate_tex(basename)

        if compiler is not None:
            compilers = ((compiler, []),)
        else:
            latexmk_args = ['--pdf']

            compilers = (
                ('latexmk', latexmk_args),
                ('pdflatex', [])
            )

        main_arguments = ['--interaction=nonstopmode', basename + '.tex']

        os_error = None

        for compiler, arguments in compilers:
            command = [compiler] + arguments + compiler_args + main_arguments

            try:
                output = subprocess.check_output(command,
                                                 stderr=subprocess.STDOUT)
            except (OSError, IOError) as e:
                # Use FileNotFoundError when python 2 is dropped
                os_error = e

                if os_error.errno == errno.ENOENT:
                    # If compiler does not exist, try next in the list
                    continue
                raise(e)
            except subprocess.CalledProcessError as e:
                # For all other errors print the output and raise the error
                print(e.output.decode())
                raise(e)
            else:
                if not silent:
                    print(output.decode())

            if clean:
                try:
                    # Try latexmk cleaning first
                    subprocess.check_output(['latexmk', '-c', basename],
                                            stderr=subprocess.STDOUT)
                except (OSError, IOError) as e:
                    # Otherwise just remove some file extensions.
                    extensions = ['aux', 'log', 'out', 'fls',
                                  'fdb_latexmk']

                    for ext in extensions:
                        try:
                            os.remove(basename + '.' + ext)
                        except (OSError, IOError) as e:
                            # Use FileNotFoundError when python 2 is dropped
                            if e.errno != errno.ENOENT:
                                raise

            if clean_tex:
                os.remove(basename + '.tex')  # Remove generated tex file

            rm_temp_dir()

            # Compilation has finished, so no further compilers have to be
            # tried
            break

        else:
            # If none of the compilers worked, raise the last error
            raise(os_error)

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

        if filepath is None:
            return self.default_filepath
        else:
            if os.path.basename(filepath) == '':
                filepath = os.path.join(filepath, os.path.basename(
                    self.default_filepath))
            return filepath

    def change_page_style(self, style):
        r"""Alternate page styles of the current page.

        Args
        ----
        style: str
            value to set for the page style of the current page
        """

        self.append(Command("thispagestyle", arguments=style))

    def change_document_style(self, style):
        r"""Alternate page style for the entire document.

        Args
        ----
        style: str
            value tp set for the document style
        """

        self.preamble.append(Command("pagestyle", arguments=style))

    def add_color(self, name, model, description):
        r"""Add a color that can be used throughout the document.

        Args
        ----
        name: str
            Name to set for the color
        model: str
            The color model to use when defining the color
        description: str
            The values to use to define the color
        """

        if self.color is False:
            self.packages.append(Package("color"))
            self.color = True

        self.preamble.append(Command("definecolor", arguments=[name,
                                                               model,
                                                               description]))

    def change_length(self, parameter, value):
        r"""Change the length of a certain parameter to a certain value.

        Args
        ----
        parameter: str
            The name of the parameter to change the length for
        value: str
            The value to set the parameter to
        """

        self.preamble.append(UnsafeCommand('setlength',
                                           arguments=[parameter, value]))

    def add_watermark(self, text, scale=1):
        """Add a watermark to the document.

        Args
        ----
        text: str
            The text to be displayed on the watermark
        scale: float
            The scale of the watermark
        """

        if not self.watermark:
            self.packages.append(Package("draftwatermark"))
            self.preamble.append(Command(command="SetWatermarkText",
                                         arguments=text))
            self.preamble.append(Command(command="SetWatermarkScale",
                                         arguments=scale))
