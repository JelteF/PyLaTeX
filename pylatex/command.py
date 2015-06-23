# -*- coding: utf-8 -*-
"""
This module implements a class that implements a latex command.

This can be used directly or it can be inherrited to make an easier interface
to it.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .parameters import Arguments, Options
from .base_classes import BaseLaTeXClass


class Command(BaseLaTeXClass):

    r"""
    A class that represents a command.

    :param command:
    :param arguments:
    :param options:
    :param packages:

    :type command: str
    :type arguments: str or list or :class:`pylatex.parameters.Arguments` \
        instance
    :type options: str or list or :class:`pylatex.parameters.Options` instance
    :type packages: list


    >>> Command('documentclass',
    >>>         options=Options('12pt', 'a4paper', 'twoside'),
    >>>         arguments='article').dumps()
    '\documentclass[12pt,a4paper,twoside]{article}'

    """

    def __init__(self, command, arguments=None, options=None, packages=None):
        self.command = command

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

        super().__init__(packages)

    def __key(self):
        """Return a hashable key, representing the command.

        :return:
        :rtype: tuple
        """

        return self.command, self.arguments, self.options

    def __eq__(self, other):
        """Compare two commands.

        :param other: A command

        :type other: :class:`command.Command` instance

        :return:
        :rtype: bool
        """
        # TODO: check if types match

        return self.__key() == other.__key()

    def __hash__(self):
        """Return hash of the command.

        :return:
        :rtype: int
        """

        return hash(self.__key())

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        :return:
        :rtype: str
        """

        return '\\{command}{options}{arguments}'.\
            format(command=self.command, options=self.options.dumps(),
                   arguments=self.arguments.dumps())
