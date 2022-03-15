from pylatex.base_classes import LatexObject
from pytest import raises


class BadObject(LatexObject):
    pass


def test_latex_object():
    with raises(TypeError):
        LatexObject()


def test_bad_object():
    with raises(TypeError):
        BadObject()
