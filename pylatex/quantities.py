# -*- coding: utf-8 -*-
"""
This module implements the classes that deals with quantities objects.

It requires the latex package SIunitx.

..  :copyright: (c) 2015 by Björn Dahlgren.
    :license: MIT, see License for more details.
"""

from operator import itemgetter

from .base_classes import Command, Options
from .package import Package
from .utils import NoEscape


def _dimensionality_to_siunitx(dim):
    string = ''
    items = dim.items()
    for unit, power in sorted(items, key=itemgetter(1), reverse=True):
        if power < 0:
            substring = r'\per'
            power = -power
        elif power == 0:
            continue
        else:
            substring = ''
        substring += '\\' + unit.name
        if power > 1:
            substring += r'\tothe{' + str(power) + '}'
        string += substring
    return NoEscape(string)


class Quantity(Command):
    """A class representing quantities."""

    packages = [Package('siunitx')]

    def __init__(self, quantity, options=None, *, format_cb=None):
        """
        Args
        ----
        quantity: `quantities.quantity.Quantity`
            The quantity that should be displayed
        options: None, str, list or `~.Options`
            Options of the command. These are placed in front of the arguments.
        format_cb: callable
            A function which formats the number in the quantity. By default
            this uses `numpy.array_str`.

        Examples
        --------
        >>> import quantities as pq
        >>> speed = 3.14159265 * pq.meter / pq.second
        >>> Quantity(speed, options={'round-precision': 3, 'round-mode': 'figures'})
        '\\SI[round-mode=figures,round-precision=3]{3.14159265}{\meter\per\second}'

        """
        import numpy as np

        self.quantity = quantity
        self._format_cb = format_cb

        if format_cb is None:
            magnitude_str = np.array_str(quantity.magnitude)
        else:
            magnitude_str = format_cb(quantity.magnitude)
        unit_str = _dimensionality_to_siunitx(quantity.dimensionality)
        if options is not None:
            options = Options(options)
            options._escape = False  # siunitx uses dashes in kwargs
        super().__init__(command='SI', arguments=(magnitude_str, unit_str),
                         options=options)
