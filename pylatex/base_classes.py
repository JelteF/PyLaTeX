# -*- coding: utf-8 -*-
"""
    pylatex.base_classes
    ~~~~~~~~~~~~~~~~~~~~

    This module implements base classes with inheritable functions for other
    LaTeX classes.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
from jinja2.loaders import PackageLoader

try:
    from collections import UserList
except ImportError:
    from UserList import UserList
from ordered_set import OrderedSet
import six
from pylatex.utils import dumps_list

from six import StringIO

from jinja2 import Template, Environment

class BaseLaTeXClass(object):

    """A class that has some basic functions for LaTeX functions."""

    def __init__(self, packages=None):
        if packages is None:
            packages = []

        self.packages = OrderedSet(packages)

    def dumps(self):
        """Represents the class as a string in LaTeX syntax."""

    def dump(self, file_):
        """Writes the LaTeX representation of the class to a file."""
        file_.write(self.dumps())

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax."""
        return dumps_list(self.packages)

    def dump_packages(self, file_):
        """Writes the LaTeX representation of the packages to a file."""
        file_.write(self.dumps_packages())

	

    def __str__(self):
        return self.dumps()

    if six.PY2:

        def __unicode__(self):
            return self.dumps()


class Token(BaseLaTeXClass):
    def __init__(self, token):
        super(Token, self).__init__()
        self.token = token

    def dumps(self):
        return self.token


class Dimension(BaseLaTeXClass):
    __DIMENSION_UNITS = [
        'pt', 'mm', 'cm', 'in', 'ex', 'em', "baselineskip", "baselineskip",
        "columnsep", "columnwidth", "evensidemargin", "linewidth",
        "oddsidemargin", "paperwidth", "paperheight", "parindent",
        "parskip", "tabcolsep", "textheight", "textwidth", "topmargin",
        "unitlength",
    ]
    def __init__(self, size, unit):
        super(Dimension, self).__init__()
        self.width = size
        if str(unit) not in self.__DIMENSION_UNITS:
            raise ValueError("Unknown dimension unit")
        self.unit = unit

    def dumps(self):
        return u"{d.width}\\{d.unit}".format(d=self)


class TemplatedLatexMixin(object):

    TEMPLATE_NAME = None

    ENV = Environment(
         '<%', '%>',
         '<<', '>>',
         '%%%', '%%%',
        trim_blocks=True,
        lstrip_blocks=True,
        loader=PackageLoader('pylatex')
    )

    def dump_contents(self):
        return dumps_list(self)

    def dumps(self):
        u"""Represents the class as a string in LaTeX syntax."""
        file = StringIO()
        self.dump(file)
        return file.getvalue()

    def dump(self, file_):
        u"""Writes the LaTeX representation of the class to a file."""

        template = self.ENV.get_template(self.TEMPLATE_NAME)
        for token in template.generate(s=self):
            file_.write(token)


class TemplatedLatexClass(TemplatedLatexMixin, BaseLaTeXClass):
    pass


class BaseLaTeXContainer(BaseLaTeXClass):

    u"""A base class that can cointain other LaTeX content."""

    def __init__(self, data=None, packages=None):
        if data is None:
            data = []

        self.data = data

        super(BaseLaTeXContainer,self).__init__(packages=packages)

    def append(self, item):
        self.data.append(item)

    def __iter__(self):
        """
        Iterates over appened items
        """
        return iter(self.data)

    def dumps(self):
        """Represents the container as a string in LaTeX syntax."""
        self.propegate_packages()

    def propegate_packages(self):
        """Makes sure packages get propegated."""
        for item in self.data:
            if isinstance(item, BaseLaTeXContainer):
                item.propegate_packages()
            if isinstance(item, BaseLaTeXClass):
                for p in item.packages:
                    self.packages.add(p)

    def dumps_packages(self):
        """Represents the packages needed as a string in LaTeX syntax."""
        self.propegate_packages()
        return dumps_list(self.packages)

class Options(BaseLaTeXContainer, UserList):
    """

    Class implementing generic latex options, it supports normal positional
    options, as well as key-value pairs.

    >>> print(Options().dumps())
    <BLANKLINE>
    >>> print(Options('a', 'b', 'c').dumps())
    [a,b,c]
    >>> print(Options('a', 'b', 'c', width="10\em").dumps())
    [a,b,c,width=10\em]
    >>> print(Options(width=Dimension(10, 'textwidth')).dumps())
    [width=10\\textwidth]
    """

    @classmethod
    def create(cls, object):
        if object is None:
            return Options()
        if isinstance(object, (list, tuple)):
            return Options(*object)
        if isinstance(object, Options):
            return object
        if isinstance(object, six.string_types):
            return Token(object)

    def __init__(self, *args, **kwargs):
        super(BaseLaTeXContainer, self).__init__()
        self.options = list(args)
        self.data = self.options
        self.option_map = kwargs

    def __getitem__(self, item):
        return self.option_map[item]

    def __setitem__(self, key, value):
        self.option_map[key] = value

    def dumps(self):
        items = []
        items.extend(self.options)
        items.extend([u"{k}={v}".format(k=k,v=v) for k, v in self.option_map.items()])
        if len(items) == 0:
            return u""
        else:
            return u"[{}]".format(u",".join(items))

class BaseLaTeXNamedContainer(BaseLaTeXContainer):

    """A base class for containers with one of a basic begin end syntax"""

    def __init__(self, name, data=None, packages=None, options=None):
        self.name = name
        self.options = Options.create(options)

        super(BaseLaTeXNamedContainer, self).__init__(data=data, packages=packages)

    def dumps(self):
        """Represents the named container as a string in LaTeX syntax."""
        string = r'\begin{' + self.name + '}\n'

        string += self.options.dumps()

        string += dumps_list(self)

        string += r'\end{' + self.name + '}\n'

        super(BaseLaTeXNamedContainer, self).dumps()

        return string

class BaseTemplatedLaTeXNamedContainer(TemplatedLatexMixin, BaseLaTeXNamedContainer):
    """
    >>> named_containser = BaseTemplatedLaTeXNamedContainer("test", options=["a", "b"])
    >>> print(named_containser.dumps()) #doctest: +NORMALIZE_WHITESPACE
    \\begin{test}[a,b]
    \\end{test}
    """
    TEMPLATE_NAME = "enviorment.tex"

    def __init__(self, name, data=None, packages=None, options=None):
        BaseLaTeXNamedContainer.__init__(self, name, data, packages, options)




