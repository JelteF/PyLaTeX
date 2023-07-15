from pytest import raises

from pylatex.base_classes import LatexObject


class BadObject(LatexObject):
    pass


def test_latex_object():
    with raises(TypeError):
        LatexObject()


def test_bad_object():
    with raises(TypeError):
        BadObject()
