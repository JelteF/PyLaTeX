#!/usr/bin/env python

"""
Test to check if configuration changes have effect.

..  :copyright: (c) 2016 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import pylatex.config as cf
from pylatex import Document


def test():
    assert type(cf.active) == cf.Default
    cf.active = cf.Version1()
    assert cf.active.indent
    assert Document()._indent

    cf.active = cf.Version1(indent=False)
    assert not cf.active.indent
    assert not Document()._indent

    with cf.Version1().use():
        assert cf.active.indent
        assert Document()._indent

    assert not cf.active.indent
    assert not Document()._indent

    with cf.active.change(indent=True):
        assert cf.active.indent
        assert Document()._indent

    assert not cf.active.indent
    assert not Document()._indent


if __name__ == "__main__":
    test()
