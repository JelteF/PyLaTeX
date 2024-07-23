#!/usr/bin/env python

import os

from pylatex.utils import fix_filename


def test_no_dots():
    fname = "aaa"
    assert fix_filename(fname) == fname


def test_one_dot():
    fname = "aa.a"
    assert fix_filename(fname) == fname


def test_two_dots():
    fname = "aa.a.a"
    original_os_name = os.name
    try:
        os.name = "posix"
        assert fix_filename(fname) == "{aa.a}.a"
        os.name = "nt"
        assert fix_filename(fname) == "aa.a.a"
    finally:
        os.name = original_os_name


def test_three_dots():
    fname = "abc.def.fgh.ijk"
    assert fix_filename(fname) == "{abc.def.fgh}.ijk"


def test_path_and_three_dots():
    fname = "/auu/bcd/abc.def.fgh.ijk"
    assert fix_filename(fname) == "/auu/bcd/{abc.def.fgh}.ijk"


def test_dots_in_path_none_in_filename():
    fname = "/au.u/b.c.d/abc"
    assert fix_filename(fname) == "/au.u/b.c.d/abc"


def test_dots_in_path_one_in_filename():
    fname = "/au.u/b.c.d/abc.def"
    assert fix_filename(fname) == "/au.u/b.c.d/abc.def"


def test_dots_in_path_and_multiple_in_filename():
    fname = "/au.u/b.c.d/abc.def.fgh.ijk"
    assert fix_filename(fname) == "/au.u/b.c.d/{abc.def.fgh}.ijk"


def test_tilde_in_filename():
    fname = "/etc/local/foo.bar.baz/foo~1/document.pdf"
    assert (
        fix_filename(fname) == r"\detokenize{/etc/local/foo.bar.baz/foo~1/document.pdf}"
    )
