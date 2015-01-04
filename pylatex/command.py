# -*- coding: utf-8 -*-
"""
    pylatex.command
    ~~~~~~~~~~~~~~~

    This module implements a class that implements a latex command. This can be
    used directly or it can be inherrited to make an easier interface to it.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import BaseLaTeXClass
from .utils import dumps_list


class Command(BaseLaTeXClass):

    """A class that represents a command"""

    def __init__(self, command, argument=None, arguments=None, option=None,
                 options=None, **kwargs):
        self.command = command

        if argument is None and arguments is None:
            self.arguments = []
        elif arguments is None:
            self.arguments = [argument]
        elif argument is None:
            self.arguments = arguments
        else:
            raise ValueError("argument and arguments can not both have a "
                             "value")

        if option is None and options is None:
            self.options = []
        elif options is None:
            self.options = [option]
        elif option is None:
            self.options = options
        else:
            raise ValueError("option and options can not both have a value")
        super().__init__(kwargs)

    def __key(self):
        return (self.command, tuple(self.arguments), tuple(self.options))

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def dumps(self):
        """Represents the command as a string in LaTeX syntax."""
        if len(self.options) == 0:
            options = ''
        else:
            options = '[' + dumps_list(self.options, token=',') + ']'

        if len(self.arguments) == 0:
            arguments = ''
        else:
            arguments = '{' + dumps_list(self.arguments, token='}{') + '}'

        return '\\' + self.command + options + arguments + '\n'
