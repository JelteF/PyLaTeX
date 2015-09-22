# -*- coding: utf-8 -*-
"""
This module implements the base LaTeX object.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from ordered_set import OrderedSet
from pylatex.utils import dumps_list
from abc import abstractmethod, ABCMeta


class _CreatePackages(ABCMeta):
    def __init__(cls, name, bases, d):  # noqa
        packages = OrderedSet()

        for b in bases:
            if hasattr(b, 'packages'):
                packages |= b.packages

        if 'packages' in d:
            packages |= d['packages']

        cls.packages = packages

        super().__init__(name, bases, d)


class LatexObject(metaclass=_CreatePackages):

    """The class that every other LaTeX class is a subclass of.

    This class implements the main methods that every LaTeX object needs. For
    conversion to LaTeX formatted strings it implements the dumps, dump and
    generate_tex methods. It also provides the methods that can be used to
    represent the packages required by the LatexObject.
    """

    _latex_name = None

    def __init__(self):
        # TODO: only create a copy of packages when it will
        # Create a copy of the packages attribute, so changing it in an
        # instance will not change the class default.
        self.packages = self.packages.copy()

    @property
    def latex_name(self):
        """The name of the class used in LaTeX.

        It can be `None` when the class doesn't have a name.
        """
        if self._latex_name is not None:
            return self._latex_name
        return self.__class__.__name__.lower()

    @latex_name.setter
    def latex_name(self, value):
        self._latex_name = value

    @abstractmethod
    def dumps(self):
        """Represent the class as a string in LaTeX syntax.

        This method should be implemented by any class that subclasses this
        class.
        """

    def dump(self, file_w):
        """Write the LaTeX representation of the class to a file.

        Args
        ----
        file_w: io.TextIOBase
            The file object in which to save the data

        """

        file_w.write(self.dumps())

    def generate_tex(self, filepath):
        """Generate a .tex file.

        Args
        ----
        filepath: str
            The name of the file (without .tex)
        """

        with open(filepath + '.tex', 'w', encoding='utf-8') as newf:
            self.dump(newf)

    def dumps_packages(self):
        """Represent the packages needed as a string in LaTeX syntax.

        Returns
        -------
        list
        """

        return dumps_list(self.packages)

    def dump_packages(self, file_w):
        """Write the LaTeX representation of the packages to a file.

        Args
        ----
        file_w: io.TextIOBase
            The file object in which to save the data

        """

        file_w.write(self.dumps_packages())
