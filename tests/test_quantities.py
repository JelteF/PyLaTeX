# -*- coding: utf-8 -*-
import quantities as pq

from pylatex.quantities import _dimensionality_to_siunitx, Quantity


def test_quantity():
    v = 1 * pq.m/pq.s

    q1 = Quantity(v)
    assert q1.dumps() == r'\SI{1.0}{\meter\per\second}'

    q2 = Quantity(v, format_cb=lambda x: str(int(x)))
    assert q2.dumps() == r'\SI{1}{\meter\per\second}'


def test_dimensionality_to_siunitx():
    assert _dimensionality_to_siunitx((pq.volt/pq.kelvin).dimensionality) == \
        r'\volt\per\Kelvin'

if __name__ == '__main__':
    test_quantity()
    test_dimensionality_to_siunitx()
