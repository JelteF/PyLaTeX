#! /usr/bin/env python3
"""This module implements LaTeX multicol package."""

from pylatex.utils import NoEscape
from .base_classes import Environment
from .package import Package


class MultiCols(Environment):
    """The class that represents multicols."""

    packages = [Package('multicol')]

    def __init__(self, number):
        """
        Initialize class instance.

        Args
        ----
        number: int
            The number of columns in multicols.
        """
        self.number = number
        super().__init__(arguments=NoEscape(number))
