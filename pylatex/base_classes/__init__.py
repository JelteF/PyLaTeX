"""
Baseclasses that can be used to create classes representing LaTeX objects.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .command import (
    Arguments,
    Command,
    CommandBase,
    Options,
    SpecialArguments,
    SpecialOptions,
    UnsafeCommand,
)
from .containers import Container, ContainerCommand, Environment
from .float import Float
from .latex_object import LatexObject

# Old names of the base classes for backwards compatibility
BaseLaTeXClass = LatexObject
BaseLaTeXContainer = Container
BaseLaTeXNamedContainer = Environment
