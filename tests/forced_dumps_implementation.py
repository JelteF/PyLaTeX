from pylatex.base_classes import LatexObject
from nose.tools import raises


class BadObject(LatexObject):
    pass


@raises(TypeError)
def test_latex_object():
    LatexObject()


@raises(TypeError)
def test_bad_object():
    BadObject()
