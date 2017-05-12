# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import LatexObject, Environment, Command, Options
from .package import Package
import re


class TikZ(Environment):
    """Basic TikZ container class."""

    _latex_name = 'tikzpicture'
    packages = [Package('tikz')]


class Axis(Environment):
    """PGFPlots axis container class, this contains plots."""

    packages = [Package('pgfplots'), Command('pgfplotsset', 'compat=newest')]

    def __init__(self, options=None, *, data=None):
        """
        Args
        ----
        options: str, list or `~.Options`
            Options to format the axis environment.
        """

        super().__init__(options=options, data=data)


class TikZScope(Environment):
    """TikZ Scope Environment."""

    _latex_name = 'scope'


class TikZCoordinate(object):
    """A General Purpose Coordinate Class."""

    _coordinate_str_regex = re.compile(r'(\+\+)?\(\s*(-?[0-9]+(\.[0-9]+)?)\s*'
                                       ',\s*(-?[0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, x, y, relative=False):
        self._x = x
        self._y = y
        self.relative = relative

    def __repr__(self):
        if self.relative:
            ret_str = '++'
        else:
            ret_str = ''
        return ret_str + '({},{})'.format(self._x, self._y)

    def dumps(self):
        return self.__repr__()

    @classmethod
    def from_str(cls, coordinate):
        """Builds a TikZCoordinate object from a string."""

        m = cls._coordinate_str_regex.match(coordinate)

        if m is None:
            raise ValueError('invalid coordinate string')

        if m.group(1) == '++':
            relative = True
        else:
            relative = False

        return TikZCoordinate(
            float(m.group(2)), float(m.group(4)), relative=relative)

    # todo: math, etc


class TikZObject(LatexObject):
    """Abstract Class that most TikZ Objects inherits from."""

    def __init__(self, options=None):
        super(TikZObject, self).__init__()
        self.options = options


class TikZNodeAnchor(object):
    def __init__(self, node_handle, anchor_name):
        self.handle = node_handle
        self.anchor = anchor_name

    def dumps(self):
        return '({}.{})'.format(self.handle, self.anchor)


class TikZNode(TikZObject):
    """A class that represents a TiKZ node."""

    _possible_anchors = ['north', 'south', 'east', 'west']

    def __init__(self, handler=None, options=None, at=None, text=None):

        super(TikZNode, self).__init__(options=options)

        self.handler = handler

        if isinstance(at, (TikZCoordinate, type(None))):
            self._node_position = at
        else:
            raise TypeError(
                'at parameter must be an object of the'
                'TikzCoordinate class')

        self._node_text = text

    def dumps(self):

        ret_str = []
        ret_str.append(Command('node', options=self.options).dumps())

        if self.handler is not None:
            ret_str.append('({})'.format(self.handler))

        if self._node_position is not None:
            ret_str.append('at {}'.format(str(self._position)))

        if self._node_text is not None:
            ret_str.append('{{{text}}};'.format(text=self._node_text))
        else:
            ret_str.append('{};')

        return ' '.join(ret_str)

    def get_anchor_point(self, anchor_name):
        if anchor_name in self._possible_anchors:
            return TikZNodeAnchor(self.handler, anchor_name)
        else:
            try:
                anchor = int(anchor_name.split('_')[1])
            except:
                anchor = None

            if anchor is not None:
                return TikZNodeAnchor(self.handler, str(anchor))

        raise ValueError('Invalid anchor name: "{}"'.format(anchor_name))

    def __getattr__(self, attr_name):
        try:
            point = self.get_anchor_point(attr_name)
            return point
        except ValueError:
            pass

        raise AttributeError(
            'Invalid attribute requested: "{}"'.format(attr_name))


class TikZUserPath(LatexObject):
    def __init__(self, path_type, options=None):
        super(TikZUserPath, self).__init__()
        self.path_type = path_type
        self.options = options

    def dumps(self):

        ret_str = self.path_type

        if self.options is not None:
            ret_str += self.options.dumps()

        return ret_str


class TikZPathList(object):
    """Represents a path drawing."""

    _legal_path_types = ['--', '-|', '|-', 'to',
                         'rectangle', 'circle',
                         'arc', 'edge']

    def __init__(self, *args):

        self._last_item_type = None
        self._arg_list = []

        # parse list and verify legality
        self._parse_arg_list(args)

    def append(self, item):
        self._parse_next_item(item)

    def _parse_next_item(self, item):
        # assume first item is point type
        if self._last_item_type is None:
            try:
                _item = self._parse_point(item)
                self._arg_list.append(_item)
                self._last_item_type = 'point'
            except TypeError:
                # not a point, do something
                raise TypeError(
                    'First element of path list must be a node identifier'
                    ' or coordinate'
                )
        elif self._last_item_type is 'point':
            # point after point is permitted, doesnt draw
            try:
                _item = self._parse_point(item)
                self._arg_list.append(_item)
                self._last_item_type = 'point'
                return
            except ValueError:
                # not a point, try path
                pass

            # will raise typeerror if wrong
            _item = self._parse_path(item)
            self._arg_list.append(_item)
            self.last_item_type = 'path'
        elif self._last_item_type is 'path':
            # only point allowed after path
            _item = self._parse_point(item)
            self._arg_list.append(_item)
            self._last_item_type = 'point'

    def _parse_arg_list(self, args):

        for item in args:
            self._parse_next_item(item)

    @classmethod
    def _parse_path(cls, path):
        if isinstance(path, str):
            if path in cls._legal_path_types:
                return TikZUserPath(path)
            raise ValueError('Illegal user path type: "{}"'.format(path))
        elif isinstance(path, TikZUserPath):
            return path

        raise TypeError('Only string or TikZUserPath types are allowed')

    @staticmethod
    def _parse_point(point):
        if isinstance(point, str):
            try:
                return TikZCoordinate.from_str(point)
            except ValueError:
                raise ValueError('Illegal point string: "{}"'.format(point))
        elif isinstance(point, TikZCoordinate):
            return point
        elif isinstance(point, tuple):
            return TikZCoordinate(*point)
        elif isinstance(point, TikZNode):
            return '({})'.format(point.handler)
        elif isinstance(point, TikZNodeAnchor):
            return point.dumps()

        raise TypeError('Only str, tuple, TikZCoordinate,'
                        'TikZNode or TikZNodeAnchor types are allowed')

    def dumps(self):

        ret_str = []
        for item in self._arg_list:
            if isinstance(item, TikZUserPath):
                ret_str.append(item.dumps())
            elif isinstance(item, TikZCoordinate):
                ret_str.append(str(item))
            elif isinstance(item, str):
                ret_str.append(item)

        return ' '.join(ret_str)


class TikZPath(TikZObject):
    def __init__(self, path, options=None):
        super(TikZPath, self).__init__(options=options)

        if isinstance(path, TikZPathList):
            self.path = path
        elif isinstance(path, list):
            self.path = TikZPathList(*path)
        else:
            raise TypeError(
                'argument "path" can only be of types list or TikZPathList')

    def dumps(self):
        ret_str = [Command('path', options=self.options).dumps()]

        ret_str.append(self.path.dumps())

        return ' '.join(ret_str) + ';'


class TikZDraw(TikZPath):
    """A draw command is just a path command with the draw option."""

    def __init__(self, *args, **kwargs):
        super(TikZDraw, self).__init__(*args, **kwargs)

        # append option
        if self.options is not None:
            self.options['draw'] = None
        else:
            self.options = Options('draw')


class Plot(LatexObject):
    """A class representing a PGFPlot."""

    packages = [Package('pgfplots'), Command('pgfplotsset', 'compat=newest')]

    def __init__(self,
                 name=None,
                 func=None,
                 coordinates=None,
                 error_bar=None,
                 options=None):
        """
        Args
        ----
        name: str
            Name of the plot.
        func: str
            A function that should be plotted.
        coordinates: list
            A list of exact coordinates tat should be plotted.

        options: str, list or `~.Options`
        """

        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.error_bar = error_bar
        self.options = options

        super().__init__()

    def dumps(self):
        """Represent the plot as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        string = Command('addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += ' coordinates {%\n'

            if self.error_bar is None:
                for x, y in self.coordinates:
                    # ie: "(x,y)"
                    string += '(' + str(x) + ',' + str(y) + ')%\n'

            else:
                for (x, y), (e_x, e_y) in zip(self.coordinates,
                                              self.error_bar):
                    # ie: "(x,y) +- (e_x,e_y)"
                    string += '(' + str(x) + ',' + str(y) + \
                        ') +- (' + str(e_x) + ',' + str(e_y) + ')%\n'

            string += '};%\n%\n'

        elif self.func is not None:
            string += '{' + self.func + '};%\n%\n'

        if self.name is not None:
            string += Command('addlegendentry', self.name).dumps()

        super().dumps()

        return string
