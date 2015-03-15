# -*- coding: utf-8 -*-
"""
    pylatex.graphics
    ~~~~~~~~~~~~~~~~

    This module implements the class that deals with graphics.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path
from os import makedirs

from .utils import fix_filename, tmp_path, make_tmp
from .base_classes import BaseLaTeXNamedContainer
from .package import Package
from .command import Command



class Figure(BaseLaTeXNamedContainer):

    """A class that represents a Graphic."""

    def __init__(self, data=None, position=None, seperate_paragraph=True):
        """
        :param data:
        :param position:

        :type data: list
        :type position: str
        :param data:
        :param position:
        :param seperate_paragraph:

        :type data: list
        :type position: str
        :type seperate_paragraph: bool
        """

        packages = [Package('graphicx')]
        super().__init__('figure', data=data, packages=packages,
                         options=position,
                         seperate_paragraph=seperate_paragraph)

    def add_image(self, filename, width=r'0.8\textwidth',
                  placement=r'\centering'):
        """Adds an image.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        if placement is not None:
            self.append(placement)

        if width is not None:
            width = 'width=' + str(width)

        self.append(Command('includegraphics', options=width,
                            arguments=fix_filename(filename)))

    def add_caption(self, caption):
        """Adds a caption to the figure.

        :param caption:
        :type caption: str
        """

        self.append(Command('caption', caption))


class Plt(Figure):
    """A class that represents a plot created with matplotlib."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _save_plot(self, plt):
        """Saves the plot.

        :param plt: matplotlib.pyplot
        :type plt: module

        :return: The basename with which the plot has been saved.
        :rtype: str
        """

        make_tmp()

        basename = os.path.join(tmp_path, "plot")
        filename = "{}.pdf".format(basename)

        while os.path.isfile(filename):
            basename += "t"
            filename = "{}.pdf".format(basename)

        plt.savefig(filename)

        return basename

    def add_plot(self, plt, width=r'0.8\textwidth',
                 placement=r'\centering'):
        """Adds a plot.

        :param plt: matplotlib.pyplot
        :param width: The width of the plot.
        :param placement: The placement of the plot.

        :type plt: module
        :type width: str
        :type placement: str
        """

        filename = self._save_plot(plt)

        self.add_image(filename, width, placement)
