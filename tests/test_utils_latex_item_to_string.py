#!/usr/bin/env python

from pylatex.utils import _latex_item_to_string
from pylatex.base_classes import LatexObject

TEST_STR = 'hello'


def test_string():
    name = 'abc'
    assert _latex_item_to_string(name) == name


def test_user_latex_object():
    class TestLatexObject(LatexObject):
        def dumps(self):
            return TEST_STR

    assert _latex_item_to_string(TestLatexObject()) == TEST_STR


def test_foreign_object():
    class ForeignObject(object):
        def dumps(self):
            return 15

        def __str__(self):
            return TEST_STR

    assert _latex_item_to_string(ForeignObject()) == TEST_STR
