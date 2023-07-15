#!/usr/bin/env python

from pylatex.basic import MediumText
from pylatex.utils import dumps_list


def test_mapper():
    assert (
        dumps_list(["Test", "text"], mapper=MediumText)
        == """\\begin{large}%
Test%
\\end{large}%
\\begin{large}%
text%
\\end{large}"""
    )


if __name__ == "__main__":
    test_mapper()
