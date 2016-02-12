# -*- coding: utf-8 -*-
"""
This module implements the classes that deals with quantities objects.

It requires the latex package SIunitx.

..  :copyright: (c) 2015 by Björn Dahlgren.
    :license: MIT, see License for more details.
"""

from operator import itemgetter

from .base_classes import Command
from .package import Package
from .utils import NoEscape, escape_latex


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

    def __init__(self, quantity, *, options=None, format_cb=None):
        r"""
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
        >>> Quantity(speed, options={'round-precision': 3,
        ...                          'round-mode': 'figures'})
        '\\SI[round-mode=figures,round-precision=3]{3.14159265}{\meter\per\second}'

        Uncertainties are also handled:

        >>> length = pq.UncertainQuantity(16.0, pq.meter, 0.3)
        >>> width = pq.UncertainQuantity(16.0, pq.meter, 0.4)
        >>> Quantity(length*width)
        '\\SI{256.0 +- 0.5}{\meter\tothe{2}}

        Ordinary numbers are also supported:

        >>> Avogadro_constant = 6.022140857e23
        >>> Quantity(Avogadro_constant, options={'round-precision': 3})
        '\\num[round-precision=3]{6.022e23}'

        """
        import numpy as np
        import quantities as pq

        self.quantity = quantity
        self._format_cb = format_cb

        def _format(val):
            if format_cb is None:
                try:
                    return np.array_str(val)
                except AttributeError:
                    return escape_latex(val)  # Python float and int
            else:
                return format_cb(val)

        if isinstance(quantity, pq.UncertainQuantity):
            magnitude_str = '{} +- {}'.format(
                _format(quantity.magnitude), _format(quantity.uncertainty))
        elif isinstance(quantity, pq.Quantity):
            magnitude_str = _format(quantity.magnitude)

        if isinstance(quantity, (pq.UncertainQuantity, pq.Quantity)):
            unit_str = _dimensionality_to_siunitx(quantity.dimensionality)
            super().__init__(command='SI', arguments=(magnitude_str, unit_str),
                             options=options)
        else:
            super().__init__(command='num', arguments=_format(quantity),
                             options=options)

        self.arguments._escape = False  # dash in e.g. \num{3 +- 2}
        if self.options is not None:
            self.options._escape = False  # siunitx uses dashes in kwargs
