# -*- coding: utf-8 -*-
"""
This module implements the base LaTeX object.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from ordered_set import OrderedSet
from pylatex.utils import dumps_list


class LatexObject:

    """The class that every other LaTeX class is a subclass of.

    This class implements the main methods that every LaTeX object needs. For
    conversion to LaTeX formatted strings it implements the dumps, dump and
    generate_tex methods. It also provides the methods that can be used to
    represent the packages needed.

    :param packages: :class:`pylatex.package.Package` instances

    :type packages: list

    """

    def __init__(self, packages=None):

        if packages is None:
            packages = []

        self.packages = OrderedSet(packages)

    def dumps(self):
        """Represent the class as a string in LaTeX syntax.

        This method should be implemented by any class that subclasses this
        class.
        """
        # TODO: Raise not implemented exception

    def dump(self, file_):
        """Write the LaTeX representation of the class to a file.

        :param file_: The file object in which to save the data

        :type file_: io.TextIOBase
        """

        file_.write(self.dumps())

    def generate_tex(self, filepath):
        """Generate a .tex file.

        :param filepath: the name of the file (without .tex)
        :type filepath: str
        """

        with open(filepath + '.tex', 'w', encoding='utf-8') as newf:
            self.dump(newf)

    def dumps_packages(self):
        """Represent the packages needed as a string in LaTeX syntax.

        :return:
        :rtype: list
        """

        return dumps_list(self.packages)

    def dump_packages(self, file_):
        """Write the LaTeX representation of the packages to a file.

        :param file_: The file object in which to save the data

        :type file_: io.TextIOBase
        """

        file_.write(self.dumps_packages())
