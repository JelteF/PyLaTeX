#!/usr/bin/env python

from pylatex.utils import fix_filename


fname = "aaa"
assert fix_filename(fname) == fname

fname = "aa.a"
assert fix_filename(fname) == fname

fname = "aa.a.a"
assert fix_filename(fname) == "{aa.a}.a"
