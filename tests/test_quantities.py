# -*- coding: utf-8 -*-
import quantities as pq

from pylatex.quantities import _dimensionality_to_siunitx, Quantity


def test_quantity():
    v = 1 * pq.m/pq.s

    q1 = Quantity(v)
    assert q1.dumps() == r'\SI{1.0}{\meter\per\second}'

    q2 = Quantity(v, format_cb=lambda x: str(int(x)))
    assert q2.dumps() == r'\SI{1}{\meter\per\second}'

    q3 = Quantity(v, options={'zero-decimal-to-integer': 'true'})
    ref = r'\SI[zero-decimal-to-integer=true]{1.0}{\meter\per\second}'
    assert q3.dumps() == ref


def test_quantity_float():
    q1 = Quantity(42.0)
    assert q1.dumps() == r'\num{42.0}'


def test_quantity_uncertain():
    t = pq.UncertainQuantity(7., pq.second, 1.)
    q1 = Quantity(t)
    assert q1.dumps() == r'\SI{7.0 +- 1.0}{\second}'


def test_dimensionality_to_siunitx():
    assert _dimensionality_to_siunitx((pq.volt/pq.kelvin).dimensionality) == \
        r'\volt\per\Kelvin'

if __name__ == '__main__':
    test_quantity()
    test_quantity_uncertain()
    test_dimensionality_to_siunitx()
