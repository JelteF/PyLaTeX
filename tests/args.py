#!/usr/bin/python

"""
    Calls functions with all available arguments to check whether they still
    exist. An error from this file means that the public API has been changed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as pyplot

from pylatex import Document, Section, Math, Table, Figure, SubFigure, Package, TikZ, \
    Axis, Plot, Plt, Itemize, Enumerate, Description
from pylatex.command import Command
from pylatex.numpy import Matrix, VectorName
from pylatex.utils import escape_latex, fix_filename, dumps_list, bold, \
    italic, verbatim


# Document
doc = Document(
    default_filepath='default_filepath',
    documentclass='article',
    fontenc='T1',
    inputenc='utf8',
    author='',
    title='',
    date='',
    data=None,
    maketitle=False
)

doc.append('Some text.')

doc.generate_tex(filepath='')
doc.generate_pdf(filepath='', clean=True)

# SectionBase
s = Section(title='', numbering=True, data=None)

# Math
m = Math(data=None, inline=False)

# Table
t = Table(table_spec='|c|c|', data=None, pos=None, table_type='tabular')

t.add_hline(start=None, end=None)

t.add_row(cells=(1, 2), escape=False)

t.add_multicolumn(size=2, align='|c|', content='Multicol', cells=None,
                  escape=False)

t.add_multirow(size=3, align='*', content='Multirow', hlines=True, cells=None,
               escape=False)

# Command
c = Command(command='documentclass', arguments=None, options=None,
            packages=None)
# Figure
f = Figure(data=None, position=None)

f.add_image(filename='', width=r'0.8\textwidth', placement=r'\centering')

f.add_caption(caption='')

# Subfigure
s = SubFigure(data=None, position=None,
              width=r'0.45\linewidth', seperate_paragraph=False)

s.add_image(filename='', width='r\linewidth',
            placement=None)

s.add_caption(caption='')

# Plt
plot = Plt(data=None, position=None)

x = [0, 1, 2, 3, 4, 5, 6]
y = [15, 2, 7, 1, 5, 6, 9]

pyplot.plot(x, y)

plot.add_plot(plt=pyplot, width=r'0.8\textwidth', placement=r'\centering')
plot.add_caption(caption='I am a caption.')

# Numpy
v = VectorName(name='')

M = np.matrix([[2, 3, 4],
               [0, 0, 1],
               [0, 0, 2]])
m = Matrix(matrix=M, name='', mtype='p', alignment=None)

# Package
p = Package(name='', base='usepackage', options=None)

# PGFPlots
tikz = TikZ(data=None)

a = Axis(data=None, options=None)

p = Plot(name=None, func=None, coordinates=None, options=None)

# Utils
escape_latex(s='')

fix_filename(path='')

dumps_list(l=[], escape=False, token='\n')

bold(s='')

italic(s='')

verbatim(s='', delimiter='|')

# Lists
itemize = Itemize()
itemize.add_item(s="item")
itemize.append("append")

enum = Enumerate()
enum.add_item(s="item")
enum.append("append")

desc = Description()
desc.add_item(label="label", s="item")
desc.append("append")
