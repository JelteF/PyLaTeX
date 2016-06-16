# -*- coding: utf-8 -*-

from .base_classes import PreambleCommand, Command
from .package import Package
from .utils import NoEscape


class PageStyle(PreambleCommand):
    r"""Allows the creation of new page styles."""

    _latex_name = "fancypagestyle"

    packages = [Package('fancyhdr')]

    def __init__(self, name, data=None, header_thickness=0,
                 footer_thickness=0):
        r"""Initialize a page style.

        Args
        ----
        name: str
            The name of the page style
        header_thickness: float
            Value to set for the line under the header
        footer_thickness: float
            Value to set for the line over the footer
        """

        self.name = name

        super().__init__(data=data, name=self.name)

        self.change_thickness(element="header", thickness=header_thickness)
        self.change_thickness(element="footer", thickness=footer_thickness)

    def change_thickness(self, element, thickness):
        r"""Change line thickness.

        Changes the thickness of the line under/over the header/footer
        to the specified thickness.

        Args
        ----
        element: str
            the name of the element to change thickness for: header, footer
        thickness: float
            the thickness to set the line to
        """

        if element == "header":
            self.data.append(Command("renewcommand",
                             arguments=[NoEscape(r"\headrulewidth"),
                                        str(thickness) + 'pt']))
        elif element == "footer":
            self.data.append(
                Command(
                    "renewcommand",
                    arguments=[
                        NoEscape(r"\footrulewidth"),
                        str(thickness) +
                        'pt']))


class Head(PreambleCommand):
    r"""Allows the creation of headers."""

    _latex_name = "fancyhead"

    def __init__(self, position, data=None):
        r"""Initialize a head object.

        Args
        ----
        position: str
            the headers position: L, C, R
        """

        self.position = position

        super().__init__(data=data, options=position)


class Foot(Head):
    r"""Allows the creation of footers."""

    _latex_name = "fancyfoot"
