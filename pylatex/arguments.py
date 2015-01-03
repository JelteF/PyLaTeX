# -*- coding: utf-8 -*-
"""
    pylatex.arguments
    ~~~~~~~

    This module implements the class that deals with tables.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
from .base_classes import BaseLaTeXClass


class Arguments(BaseLaTeXClass):
    """
        Class implementing generic latex options, it supports normal positional options, as well as key-value pairs.

        :type optional: bool
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.optional = False
        self._positional_args = list(args)
        self._key_value_args = dict(kwargs)
        super().__init__(packages=None)

    def dumps(self):
        """
        Represents the arguments as a string in LaTeX syntax to be appended to a command.

        :return:
        """
        args = []
        args.extend(self._positional_args)
        args.extend(['{k}={v}'.format(k=k, v=v) for k, v in self._key_value_args.items()])
        if len(args) <= 0:
            return ''
        if self.optional:
            string = '[{args}]'.format(args=','.join(args))
        else:
            string = '{{{args}}}'.format(args=','.join(args))
        return string

    def dump(self, file_):
        file_.write(self.dumps())
