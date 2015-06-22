# -*- coding: utf-8 -*-
"""
    pylatex.graphics
    ~~~~~~~~~~~~~~~~

    This module implements the class that deals with graphics.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path

from .utils import fix_filename, make_temp_dir
from .base_classes import BaseLaTeXNamedContainer
from .package import Package
from .command import Command
import uuid


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
        super().__init__(data=data, packages=packages,
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


class SubFigure(BaseLaTeXNamedContainer):

    """A Class that represents a subfigure from the subcaption package"""

    def __init__(self, data=None, position=None,
                 width=r'0.45\linewidth', seperate_paragraph=False):
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

        packages = [Package('subcaption')]

        super().__init__(data=data, packages=packages,
                         options=position,
                         argument=width,
                         seperate_paragraph=seperate_paragraph)

    def add_image(self, filename, width=r'\linewidth',
                  placement=None):
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
        """Adds a caption to the figure

        :param caption:
        :type caption: str
        """

        self.append(Command('caption', caption))


class Plt(Figure):
    """A class that represents a plot created with matplotlib."""

    container_name = 'figure'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _save_plot(self, plt, *args, **kwargs):
        """Saves the plot.

        :param plt: The matplotlib.pyplot module
        :type plt: matplotlib.pyplot

        :return: The basename with which the plot has been saved.
        :rtype: str
        """

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, str(uuid.uuid4()) + '.pdf')

        plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, plt, width=r'0.8\textwidth',
                 placement=r'\centering', *args, **kwargs):
        """Adds a plot.

        :param plt: The matplotlib.pyplot module
        :param width: The width of the plot.
        :param placement: The placement of the plot.

        :type plt: matplotlib.pyplot
        :type width: str
        :type placement: str
        """

        filename = self._save_plot(plt, *args, **kwargs)

        self.add_image(filename, width, placement)
