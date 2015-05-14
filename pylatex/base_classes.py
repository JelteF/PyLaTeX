# -*- coding: utf-8 -*-
"""
    pylatex.base_classes
    ~~~~~~~~~~~~~~~~~~~~

    This module implements base classes with inheritable functions for other
    LaTeX classes.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from collections import UserList
from ordered_set import OrderedSet
from pylatex.utils import dumps_list
from contextlib import contextmanager


class BaseLaTeXClass:

    """A class that has some basic functions for LaTeX functions."""

    def __init__(self, packages=None):
        """
            :param packages: :class:`pylatex.Package` instances

            :type packages: list
        """

        if packages is None:
            packages = []

        self.packages = OrderedSet(packages)

    def dumps(self):
        """Represents the class as a string in LaTeX syntax."""

    def dump(self, file_):
        """Writes the LaTeX representation of the class to a file.

            :param file_: The file object in which to save the data

            :type file_: file object
        """

        file_.write(self.dumps())

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax.

            :return:
            :rtype: list
        """

        return dumps_list(self.packages)

    def dump_packages(self, file_):
        """Writes the LaTeX representation of the packages to a file.

            :param file_: The file object in which to save the data

            :type file_: file object
        """

        file_.write(self.dumps_packages())


class BaseLaTeXContainer(BaseLaTeXClass, UserList):

    """A base class that can cointain other LaTeX content."""

    def __init__(self, data=None, packages=None):
        """
            :param data:
            :param packages: :class:`pylatex.Package` instances

            :type data: list
            :type packages: list
        """

        if data is None:
            data = []

        self.data = data
        self.real_data = data  # Always the data of this instance

        super().__init__(packages=packages)

    def dumps(self, **kwargs):
        """Represents the container as a string in LaTeX syntax.

            :return:
            :rtype: list
        """

        self.propegate_packages()

        return dumps_list(self, **kwargs)

    def propegate_packages(self):
        """Makes sure packages get propegated."""

        for item in self.data:
            if isinstance(item, BaseLaTeXClass):
                for p in item.packages:
                    self.packages.add(p)

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax.

            :return:
            :rtype: list
        """

        self.propegate_packages()

        return dumps_list(self.packages)

    @contextmanager
    def create(self, child):
        """Add a LaTeX object to current container, context-manager style.

            :param child: An object to be added to the current container
        """

        prev_data = self.data
        self.data = child.data  # This way append works appends to the child

        yield child  # allows with ... as to be used as well

        self.data = prev_data
        self.append(child)


class BaseLaTeXNamedContainer(BaseLaTeXContainer):

    """A base class for containers with one of a basic begin end syntax"""

    def __init__(self, name, options=None, argument=None,
                 seperate_paragraph=False, begin_paragraph=False,
                 end_paragrpaph=False, **kwargs):
        """
            :param name:
            :param options:
            :param argument:

            :type name: str
            :type options: str or list or :class:`parameters.Options` instance
            :type argument: str
        """

        self.name = name
        self.options = options
        self.argument = argument
        self.seperate_paragraph = seperate_paragraph
        self.begin_paragraph = begin_paragraph
        self.end_paragrpaph = end_paragrpaph

        super().__init__(**kwargs)

    def dumps(self):
        """Represents the named container as a string in LaTeX syntax.

            :return:
            :rtype: str
        """

        string = ''

        if self.seperate_paragraph or self.begin_paragraph:
            string += '\n\n'

        string += r'\begin{' + self.name + '}'

        if self.options is not None:
            string += '[' + self.options + ']'

        if self.argument is not None:
            string += '{' + self.argument + '}'

        string += '\n'

        string += super().dumps()

        string += '\n' + r'\end{' + self.name + '}'

        if self.seperate_paragraph or self.end_paragrpaph:
            string += '\n\n'

        return string
