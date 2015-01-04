# -*- coding: utf-8 -*-
"""
    pylatex.arguments
    ~~~~~~~

    This module implements the class that deals with arguments.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
from .base_classes import BaseLaTeXClass


class Arguments(BaseLaTeXClass):
    """
    A class implementing LaTex arguments. It supports normal positional arguments, as well as key-value pairs. Arguments
    can be rendered optional within square brackets ``[]`` or required within braces ``{}``.
    ::
        >>> args = Arguments('a', 'b', 'c')
        >>> args.dumps()
        '{a}{b}{c}'
        >>> args.optional = True
        >>> args.dumps()
        '[a,b,c]'
        >>> args = Arguments('clip', width=50, height='25em', trim='1 2 3 4')
        >>> args.optional = True
        >>> args.dumps()
        '[clip,trim=1 2 3 4,width=50,height=25em]'

    :param optional: Specifies whether this arguments are optional or not
    :type optional: bool
    """

    optional = False

    def __init__(self, *args, **kwargs):
        self._positional_args = list(args)
        self._key_value_args = dict(kwargs)
        super().__init__(packages=None)

    def dumps(self):
        """
        Represents the arguments as a string in LaTeX syntax to be appended to a command.

        :return: The rendered arguments
        :rtype: str
        """
        args = []
        args.extend(self._positional_args)
        args.extend(['{k}={v}'.format(k=k, v=v) for k, v in self._key_value_args.items()])
        if len(args) <= 0:
            return ''
        if self.optional:
            string = '[{args}]'.format(args=','.join(args))
        else:
            string = '{{{args}}}'.format(args='}{'.join(args))
        return string
