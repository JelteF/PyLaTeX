#!/usr/bin/env python

from pylatex.utils import fix_filename


fname = "aaa"
assert fix_filename(fname) == fname

fname = "aa.a"
assert fix_filename(fname) == fname

fname = "aa.a.a"
assert fix_filename(fname) == "{aa.a}.a"

fname = "abc.def.fgh.ijk"
assert fix_filename(fname) == "{abc.def.fgh}.ijk"

fname = "/auu/bcd/abc.def.fgh.ijk"
assert fix_filename(fname) == "/auu/bcd/{abc.def.fgh}.ijk"

fname = "/au.u/b.c.d/abc.def.fgh.ijk"
assert fix_filename(fname) == "/au.u/b.c.d/{abc.def.fgh}.ijk"

fname = "/au.u/b.c.d/abc"
assert fix_filename(fname) == "/au.u/b.c.d/abc"
fname = "/au.u/b.c.d/abc.def"
assert fix_filename(fname) == "/au.u/b.c.d/abc.def"
