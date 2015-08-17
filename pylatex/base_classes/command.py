# -*- coding: utf-8 -*-
"""
This module implements a class that implements a latex command.

This can be used directly or it can be inherrited to make an easier interface
to it.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .latex_object import LatexObject


class Command(LatexObject):

    """
    A class that represents a LaTeX command.

    Args
    ----
    command: str
        Name of the command
    arguments: None, str, list or \
            :class:`~pylatex.base_classes.command.Arguments`
        Arguments of the command
    options: None, str, list or \
            :class:`~pylatex.base_classes.command.Options`
        Arguments of the command
    packages: list of :class:`~pylatex.package.Package` instances
        A list of the packages that this command requires


    >>> Command('documentclass',
    >>>         options=Options('12pt', 'a4paper', 'twoside'),
    >>>         arguments='article').dumps()
    '\\documentclass[12pt,a4paper,twoside]{article}'

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

        Args
        ----
        other: :class:`~pylatex.base_classes.command.Command` instance
            The command to compare this command to


        Returns
        -------
        bool:
            If the two instances are equal
        """
        # TODO: check if types match

        return self.__key() == other.__key()

    def __hash__(self):
        """Calculate the hash of a command.

        Returns
        -------
        int:
            The hash of the command
        """

        return hash(self.__key())

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        Returns
        -------
        str
            The LaTeX formatted command
        """

        return '\\{command}{options}{arguments}'.\
            format(command=self.command, options=self.options.dumps(),
                   arguments=self.arguments.dumps())


class Parameters(LatexObject):

    """
    A class implementing LaTex parameters.

    It supports normal positional parameters, as well as key-value pairs.
    Parameters can be rendered optional within square brackets ``[]`` or
    required within braces ``{}``.

    >>> args = Parameters('a', 'b', 'c')
    >>> args.dumps()
    '{a}{b}{c}'
    >>> args.optional = True
    >>> args.dumps()
    '[a,b,c]'
    >>> args = Parameters('clip', width=50, height='25em', trim='1 2 3 4')
    >>> args.optional = True
    >>> args.dumps()
    '[clip,trim=1 2 3 4,width=50,height=25em]'

    :param optional: Specifies whether this parameters are optional or not
    :type optional: bool
    """

    optional = False
    # TODO: Rewrite this in a way such that the optional boolean is not needed
    # in this class

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__') and\
                not isinstance(args[0], str):
            args = args[0]

        self._positional_args = list(args)
        self._key_value_args = dict(kwargs)

        super().__init__(packages=None)

    def __key(self):
        """Generate a unique hashable key representing the parameter object.

        :return:
        :rtype: tuple
        """

        return self.optional, tuple(self.list())

    def __eq__(self, other):
        """Compare two parameters.

        :return:
        :rtype: bool
        """
        # TODO: Check if type is the same

        return self.__key() == other.__key()

    def __hash__(self):
        """Generate a hash of the parameters.

        :return:
        :rtype: int
        """

        return hash(self.__key())

    def dumps(self):
        """Represent the parameters as a string in LaTeX syntax.

        This is to be appended to a command.

        :return: The rendered parameters
        :rtype: str
        """

        params = self.list()

        if len(params) <= 0:
            return ''

        if self.optional:
            string = '[{args}]'.format(args=','.join(map(str, params)))
        else:
            string = '{{{args}}}'.format(args='}{'.join(map(str, params)))

        return string

    def list(self):
        """TODO.

        :return:
        :rtype: list
        """

        params = []
        params.extend(self._positional_args)
        params.extend(['{k}={v}'.format(k=k, v=v) for k, v in
                       self._key_value_args.items()])

        return params


class Options(Parameters):

    """TODO: write some stuff about Options."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.optional = True


class Arguments(Parameters):

    """TODO: write some stuff about Arguments."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.optional = False
