"""
A library for creating Latex files.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from . import _version
from .base_classes import Command, UnsafeCommand
from .basic import (
    FootnoteText,
    HFill,
    HugeText,
    LargeText,
    LineBreak,
    MediumText,
    NewLine,
    NewPage,
    SmallText,
    TextColor,
)
from .document import Document
from .errors import TableRowSizeError
from .figure import Figure, StandAloneGraphic, SubFigure
from .frames import FBox, MdFramed
from .headfoot import Foot, Head, PageStyle, simple_page_number
from .labelref import Autoref, Eqref, Hyperref, Label, Marker, Pageref, Ref
from .lists import Description, Enumerate, Itemize
from .math import Alignat, Math, Matrix, VectorName
from .package import Package
from .position import (
    Center,
    FlushLeft,
    FlushRight,
    HorizontalSpace,
    MiniPage,
    TextBlock,
    VerticalSpace,
)
from .quantities import Quantity
from .section import Chapter, Section, Subsection, Subsubsection
from .table import (
    ColumnType,
    LongTable,
    LongTabu,
    LongTabularx,
    MultiColumn,
    MultiRow,
    Table,
    Tabu,
    Tabular,
    Tabularx,
)
from .tikz import (
    Axis,
    Plot,
    TikZ,
    TikZCoordinate,
    TikZDraw,
    TikZNode,
    TikZNodeAnchor,
    TikZOptions,
    TikZPath,
    TikZPathList,
    TikZScope,
    TikZUserPath,
)
from .utils import NoEscape, escape_latex

__version__ = _version.get_versions()["version"]
