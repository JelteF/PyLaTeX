# -*- coding: utf-8 -*-
"""
This module implements LaTeX base classes that can be subclassed.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from collections import UserList
from pylatex.utils import dumps_list
from contextlib import contextmanager
from pylatex.base_classes import LatexObject


class Container(LatexObject, UserList):

    """A base class that groups multiple LaTeX classes.

    This class should be subclassed when a LaTeX class has content that is
    variable of variable length. It subclasses UserList, so it holds a list
    of elements that can simply be accessed by using normal list functionality,
    like indexing or appending.

    :param data:
    :param packages: :class:`pylatex.package.Package` instances

    :type data: list
    :type packages: list
    """

    # TODO: Find a way to document multiple types, in this case str as well

    def __init__(self, data=None, packages=None):

        if data is None:
            data = []
        elif not isinstance(data, list):
            # If the data is not already a list make it a list, otherwise list
            # operations will not work
            data = [data]

        self.data = data
        self.real_data = data  # Always the data of this instance

        super().__init__(packages=packages)

    def dumps(self, **kwargs):
        """Represent the container as a string in LaTeX syntax.

        :return:
        :rtype: list
        """

        self.propegate_packages()

        return dumps_list(self, **kwargs)

    def propegate_packages(self):
        """Make sure packages get propegated."""

        for item in self.data:
            if isinstance(item, LatexObject):
                if isinstance(item, Container):
                    item.propegate_packages()
                for p in item.packages:
                    self.packages.add(p)

    def dumps_packages(self):
        """Represent the packages needed as a string in LaTeX syntax.

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


class Environment(Container):

    r"""A base class for LaTeX environments.

    This class implements the basics of a LaTeX environment. A LaTeX
    environment looks like this:

    .. code-block:: latex

        \begin{environment_name}
            Some content that is in the environment
        \end{environment_name}

    The text that is used in the place of environment_name is by defalt the
    name of the class in lowercase. However, this default can be overridden by
    setting the environment_name class variable when declaring the class.

    :param name:
    :param options:
    :param arguments:

    :type name: str
    :type options: str or list or \
        :class:`~pylatex.base_classes.command.Options` instance
    :type argument: str or list or \
        :class:`~pylatex.base_classes.command.Arguments` instance
    """

    def __init__(self, options=None, arguments=None,
                 seperate_paragraph=False, begin_paragraph=False,
                 end_paragraph=False, **kwargs):
        from pylatex.parameters import Arguments, Options

        if not hasattr(self, 'container_name'):
            self.container_name = self.__class__.__name__.lower()

        if isinstance(arguments, Arguments):
            self.arguments = arguments
        elif arguments is not None:
            self.arguments = Arguments(arguments)
        else:
            self.arguments = Arguments()

        if isinstance(options, Options):
            self.options = options
        elif options is not None:
            self.options = Options(options)
        else:
            self.options = Options()

        self.seperate_paragraph = seperate_paragraph
        self.begin_paragraph = begin_paragraph
        self.end_paragraph = end_paragraph

        super().__init__(**kwargs)

    def dumps(self):
        """Represent the named container as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        string = ''

        if self.seperate_paragraph or self.begin_paragraph:
            string += '\n\n'

        string += r'\begin{' + self.container_name + '}'

        string += self.options.dumps()

        string += self.arguments.dumps()

        string += '\n'

        string += super().dumps()

        string += '\n' + r'\end{' + self.container_name + '}'

        if self.seperate_paragraph or self.end_paragraph:
            string += '\n\n'

        return string
