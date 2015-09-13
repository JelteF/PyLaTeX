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
        """Add an image to the figure.

        Args
        ----
        filename: str
            Filename of the image.
        width: str
            Width of the image in LaTeX terms.
        placement: str
            Placement of the figure, `None` is also accepted.

        """

        if placement is not None:
            self.append(placement)

        if width is not None:
            width = 'width=' + str(width)

        self.append(Command('includegraphics', options=width,
                            arguments=fix_filename(filename)))

    def _save_plot(self, *args, **kwargs):
        """Save the plot.

        Returns
        -------
        str
            The basename with which the plot has been saved.
        """

        import matplotlib.pyplot as plt

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, str(uuid.uuid4()) + '.pdf')

        plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, *args, **kwargs):
        """Add the current Matplotlib plot to the figure.

        The plot that gets added is the one that would normally be shown when
        using ``plt.show()``.

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

    """A class that represents a subfigure from the subcaption package."""

    def __init__(self, width=r'0.45\linewidth', separate_paragraph=False,
                 *args, **kwargs):
        """.

        Args
        ----
        width: str
            Width of the subfigure itself. It needs a width because it is
            inside another figure.
        separate_paragraph: bool
            By default a subfigure is not on its own paragraph since that looks
            weird inside another figure.

        """

        packages = [Package('subcaption')]

        super().__init__(packages=packages,
                         arguments=width,
                         separate_paragraph=separate_paragraph,
                         *args, **kwargs)

    def add_image(self, filename, width=r'\linewidth',
                  placement=None):
        """Add an image to the subfigure.

        Args
        ----
        filename: str
            Filename of the image.
        width: str
            Width of the image in LaTeX terms.
        placement: str
            Placement of the figure, `None` is also accepted.
        """

        super().add_image(filename, width=width, placement=placement)
