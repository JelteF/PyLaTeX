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

        self._set_parameters(arguments, 'arguments')
        self._set_parameters(options, 'options')

        super().__init__(packages)

    def _set_parameters(self, parameters, argument_type):
        parameter_cls = Arguments if argument_type == 'arguments' else Options

        if parameters is None:
            parameters = parameter_cls()
        elif not isinstance(parameters, parameter_cls):
            parameters = parameter_cls(parameters)

        setattr(self, argument_type, parameters)

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

        if isinstance(other, Command):
            return self.__key() == other.__key()

        return False

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

    TODO: Rewrite this since it should never be used separately, this class is
    only supposed to be inherrited

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

        return tuple(self._list_args_kwargs())

    def __eq__(self, other):
        """Compare two parameters.

        :return:
        :rtype: bool
        """

        return type(self) == type(other) and self.__key() == other.__key()

    def __hash__(self):
        """Generate a hash of the parameters.

        :return:
        :rtype: int
        """

        return hash(self.__key())

    def _format_contents(self, prefix, separater, suffix):
        """Format the parameters.

        The formatting is dono using the three arguments suplied to this
        function.

        Arguments
        ---------
        prefix: str
        separater: str
        suffix: str

        Returns
        -------
        str
        """

        params = self._list_args_kwargs()

        if len(params) <= 0:
            return ''

        string = prefix + separater.join(map(str, params)) + suffix

        return string

    def _list_args_kwargs(self):
        """TODO.

        Returns
        -------
        list
        """

        params = []
        params.extend(self._positional_args)
        params.extend(['{k}={v}'.format(k=k, v=v) for k, v in
                       self._key_value_args.items()])

        return params


class Options(Parameters):

    """TODO: write some stuff about Options."""

    def dumps(self):
        """Represent the parameters as a string in LaTeX syntax.

        This is to be appended to a command.

        Returns
        -------
        str
        """

        return self._format_contents('[', ',', ']')


class Arguments(Parameters):

    """TODO: write some stuff about Arguments."""

    def dumps(self):
        """Represent the parameters as a string in LaTeX syntax.

        This is to be appended to a command.

        Returns
        -------
        str
        """

        return self._format_contents('{', '}{', '}')
