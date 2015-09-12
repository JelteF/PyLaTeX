# -*- coding: utf-8 -*-
"""
This module implements the class that deals with graphics.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path

from .utils import fix_filename, make_temp_dir, _merge_packages_into_kwargs
from .base_classes import Command, Float
from .package import Package
import uuid


class Figure(Float):

    """A class that represents a Figure environment."""

    def __init__(self, *args, **kwargs):
        packages = [Package('graphicx')]
        _merge_packages_into_kwargs(packages, kwargs)

        super().__init__(*args, **kwargs)

    def add_image(self, filename, width=r'0.8\textwidth',
                  placement=r'\centering'):
        """Add an image.to the figure.

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

    def _save_plot(self, *args, **kwargs):
        """Save the plot.

        :param plt: The matplotlib.pyplot module
        :type plt: matplotlib.pyplot

        :return: The basename with which the plot has been saved.
        :rtype: str
        """

        import matplotlib.pyplot as plt

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, str(uuid.uuid4()) + '.pdf')

        plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, *args, **kwargs):
        """Add a plot.

        Args
        ----
        args:
            Arguments passed to plt.savefig for displaying the plot.
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot. In
            case these contain ``width`` or ``placement``, they will be used
            for the same purpose as in the add_image command. Namely the width
            and placement of the generated plot in the LaTeX document.
        """

        add_image_kwargs = {}

        for key in ('width', 'placement'):
            if key in kwargs:
                add_image_kwargs[key] = kwargs.pop(key)

        filename = self._save_plot(*args, **kwargs)

        self.add_image(filename, **add_image_kwargs)


class SubFigure(Figure):

    """A class that represents a subfigure from the subcaption package.

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

    def __init__(self, position=None, width=r'0.45\linewidth',
                 seperate_paragraph=False, *args, **kwargs):
        packages = [Package('subcaption')]

        super().__init__(packages=packages,
                         position=position,
                         arguments=width,
                         seperate_paragraph=seperate_paragraph,
                         *args, **kwargs)

    def add_image(self, filename, width=r'\linewidth',
                  placement=None):
        """Add an image to the subfigure.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        super().add_image(filename, width=width, placement=placement)
