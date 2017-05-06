#!/usr/bin/python


"""Test to validate that Environments uphold contract of base classes."""

from pylatex.base_classes import Environment


def test_alltt():
    class AllTT(Environment):
        escape = False
        content_separator = "\n"

    alltt = AllTT()
    alltt.append("This is alltt content\nIn two lines")
    s = alltt.dumps()
    assert s.startswith('\\begin{alltt}\nThis is'), \
        "Unexpected start of environment"
    assert s.endswith('two lines\n\\end{alltt}'), \
        "Unexpected end of environment"
