#!/usr/bin/python
from nose.tools import raises

from pylatex.base_classes import Float
from pylatex.labelref import Marker, Label, make_label


###################
#   Marker tests
###################


def test_marker_no_prefix():
    m = Marker("marker")
    assert m.dumps() == "marker", m.dumps()


def test_marker_with_prefix():
    m = Marker("marker", "prefix")
    assert m.dumps() == "prefix:marker", m.dumps()


@raises(ValueError)
def test_marker_empty():
    m = Marker("")


def test_with_dash():
    m = Marker("marker-name", "prefix")
    assert m.dumps() == "prefix:marker-name", m.dumps()


def test_marker_cleanup():
    m = Marker("%marker\n", "\\prefix#")
    assert m.dumps() == "prefix:marker", m.dumps()


###################
#   Label tests
###################


def test_label():
    l = Label(Marker("marker", "prefix"))
    assert l.dumps() == r"\label{prefix:marker}", l.dumps()

    l = Label("%invalid-marker")
    # TODO what is the expected behaviour in this case?
    assert l.dumps() == r"\label{invalid-marker}", l.dumps()


def test_make_label_pass_through():
    l = Label(Marker("marker", "prefix"))
    assert make_label(l) is l


def test_make_label_from_string():
    assert make_label("label").dumps() == r"\label{label}"
    assert make_label("prefix:label").dumps() == r"\label{prefix:label}"
    assert make_label("label", "prefix").dumps() == r"\label{prefix:label}"


def test_make_label_from_bool():
    assert make_label(True, default_name="label").dumps() == r"\label{label}"
    assert make_label(True, prefix="pre", default_name="label").dumps() == r"\label{pre:label}"

    assert make_label(False, prefix="pre", default_name="label") is None
    assert make_label(None, prefix="pre", default_name="label") is None


@raises(ValueError)
def test_make_label_from_no_name():
    make_label(True).dumps()


@raises(TypeError)
def test_make_label_from_number():
    make_label(5).dumps()


###################
#   float tests
###################

def test_float_without_label():
    f = Float()
    f.add_caption("cap")
    assert f.dumps() == "\\begin{float}%\n\\caption{cap}%\n\\end{float}", f.dumps()


def test_float_with_label():
    f = Float()
    f.add_caption("cap", Label(Marker("lbl")))
    assert f.dumps() == "\\begin{float}%\n\\caption{cap}%\n\\label{lbl}%\n\\end{float}", f.dumps()


def test_float_default_prefix():
    f = Float()
    f.add_caption("cap", "lbl")
    assert f.dumps() == "\\begin{float}%\n\\caption{cap}%\n\\label{float:lbl}%\n\\end{float}", f.dumps()
