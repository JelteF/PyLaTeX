# -*- coding: utf-8 -*-
'''
This module implements the classes that deals with quantities objects.

It requires the latex package SIunitx.

..  :copyright: (c) 2015 by Björn Dahlgren.
    :license: MIT, see License for more details.
'''

from operator import itemgetter

from .base_classes import Command
from pylatex.package import Package


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
    return string


class Quantity(Command):

    '''A class representing quantities.

    :param quantity:
    :param fmtstr:

    :type quantity: `quantities.quantity.Quantity` instance
    :type fmtstr: callable
    '''

    def __init__(self, quantity, format_cb=None):
        import numpy as np

        self.quantity = quantity
        if format_cb is None:
            magnitude_str = np.array_str(quantity.magnitude)
        else:
            magnitude_str = format_cb(quantity.magnitude)
        unit_str = _dimensionality_to_siunitx(quantity.dimensionality)
        super().__init__(command='SI', arguments=(magnitude_str, unit_str),
                         packages=[Package('siunitx')])
