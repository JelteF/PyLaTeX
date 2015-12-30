# flake8: noqa

"""
A library for creating Latex files.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .document import Document
from .math import Math, VectorName, Matrix
from .package import Package
from .section import Section, Subsection, Subsubsection
from .table import Table, MultiColumn, MultiRow, Tabular, Tabu, LongTable, \
    LongTabu
from .tikz import TikZ, Axis, Plot
from .figure import Figure, SubFigure
from .lists import Enumerate, Itemize, Description
from .quantities import Quantity
from .base_classes import Command, UnsafeCommand
from .utils import NoEscape
from .errors import TableRowSizeError

__version__ = str('1.0.1dev')
