# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .base_classes import LatexObject, Environment, Command, Options, Container
from .package import Package
import re
import math


class TikZOptions(Options):
    """Options class, do not escape."""

    escape = False

    def append_positional(self, option):
        """Add a new positional option."""

        self._positional_args.append(option)


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


class TikZCoordinate(LatexObject):
    """A General Purpose Coordinate Class."""

    _coordinate_str_regex = re.compile(r'(\+\+)?\(\s*(-?[0-9]+(\.[0-9]+)?)\s*'
                                       r',\s*(-?[0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, x, y, relative=False):
        """
        Args
        ----
        x: float or int
            X coordinate
        y: float or int
            Y coordinate
        relative: bool
            Coordinate is relative or absolute
        """
        self._x = float(x)
        self._y = float(y)
        self.relative = relative
        self.to_stop = False

    def __repr__(self):
        if self.relative:
            ret_str = '++'
        else:
            ret_str = ''
        return ret_str + '({},{})'.format(round(self._x,3), round(self._y,3))

    def dumps(self):
        """Return representation."""

        return self.__repr__()

    def __iter__(self):
        return iter((self._x, self._y))


    @classmethod
    def from_str(cls, coordinate):
        """Build a TikZCoordinate object from a string."""

        m = cls._coordinate_str_regex.match(coordinate)

        if m is None:
            raise ValueError('invalid coordinate string')

        if m.group(1) == '++':
            relative = True
        else:
            relative = False

        return cls(
            float(m.group(2)), float(m.group(4)), relative=relative)

    def __eq__(self, other):
        if isinstance(other, tuple):
            # if comparing to a tuple, assume it to be an absolute coordinate.
            other_relative = False
            other_x = float(other[0])
            other_y = float(other[1])
        elif isinstance(other, TikZCoordinate):
            other_relative = other.relative
            other_x = other._x
            other_y = other._y
        else:
            raise TypeError('can only compare tuple and TiKZCoordinate types')

        # prevent comparison between relative and non relative
        # by returning False
        if (other_relative != self.relative):
            return False

        # return comparison result
        return (other_x == self._x and other_y == self._y)

    def _arith_check(self, other):
        if isinstance(other, tuple):
            other_coord = TikZCoordinate(*other)
        elif isinstance(other, TikZCoordinate):
            if other.relative is True or self.relative is True:
                raise ValueError('refusing to add relative coordinates')
            other_coord = other
        else:
            raise TypeError('can only add tuple or TiKZCoordinate types')

        return other_coord

    def __add__(self, other):
        other_coord = self._arith_check(other)
        return TikZCoordinate(self._x + other_coord._x,
                              self._y + other_coord._y)

    def __radd__(self, other):
        self.__add__(other)

    def __sub__(self, other):
        other_coord = self._arith_check(other)
        return TikZCoordinate(self._x - other_coord._y,
                              self._y - other_coord._y)

    def distance_to(self, other):
        """Euclidean distance between two coordinates."""

        other_coord = self._arith_check(other)
        return math.sqrt(math.pow(self._x - other_coord._x, 2) +
                         math.pow(self._y - other_coord._y, 2))


class TikZPolarCoordinate(TikZCoordinate):
    """Class representing the Tikz polar coordinate specification"""

    _coordinate_str_regex = re.compile(r'(\+\+)?\(\s*(-?[0-9]+(\.[0-9]+)?)\s*'
                                       r':\s*([0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, angle, radius, relative=False):
        """
        angle: float or int
            angle in degrees
        radius: float or int, non-negative
            radius from orig
        relative: bool
            Coordinate is relative or absolute

        """
        if radius < 0:
            raise ValueError("Radius must be positive")
        self._radius = float(radius)
        self._angle = float(angle)
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        super(TikZPolarCoordinate, self).__init__(x, y, relative=relative)

    def __repr__(self):
        if self.relative:
            ret_str = '++'
        else:
            ret_str = ''
        return ret_str + '({}:{})'.format(self._angle, self._radius)


class TikZArcSpecifier(LatexObject):
    """A class to represent the tikz arc specifier (ang1: ang2: rad)"""

    _str_verif_regex = re.compile(r'(\+\+)?\('
                                  r'\s*(-?[0-9]+(\.[0-9]+)?)\s*:'
                                  r'\s*(-?[0-9]+(\.[0-9]+)?)\s*:'
                                  r'\s*([0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, start_ang, finish_ang, radius, relative=False, force_far_direction=False):
        """
        start_ang: float or int
            angle in degrees
        radius: float or int
            radius from orig
        relative: bool
            Coordinate is relative or absolute
        force_far_direction: bool
            forces arc to go in the longer direction around circumference

        """
        if force_far_direction:
            # forcing an extra rotation around
            if start_ang > finish_ang:
                start_ang -= 360
            else:
                finish_ang -= 360

        self._radius = float(radius)
        self._start_ang = float(start_ang)
        self._finish_ang = float(finish_ang)
        self._relative = relative

    def __repr__(self):
        if self._relative:
            ret_str = "++"
        else:
            ret_str = ""
        return ret_str + "({}:{}:{})".format(
            self._start_ang, self._finish_ang, self._radius)

    def dumps(self):
        """Return a representation. Alias for consistency."""

        return self.__repr__()

    @classmethod
    def from_str(cls, arc):
        """Build a TikZArcSpecifier object from a string."""
        m = cls._str_verif_regex.match(arc)

        if m is None:
            raise ValueError('invalid arc string')
        if m.group(1) =='++':
            relative = True
        else:
            relative = False

        return cls(float(m.group(2)), float(m.group(4)), float(m.group(6)),
            relative=relative)


class TikZObject(Container):
    """Abstract Class that most TikZ Objects inherits from."""

    def __init__(self, options=None):
        """
        Args
        ----
        options: list
            Options pertaining to the object
        """

        super(TikZObject, self).__init__()
        self.options = options


class TikZNodeAnchor(LatexObject):
    """Representation of a node's anchor point."""

    def __init__(self, node_handle, anchor_name):
        """
        Args
        ----
        node_handle: str
            Node's identifier
        anchor_name: str
            Name of the anchor
        """

        self.handle = node_handle
        self.anchor = anchor_name

    def __repr__(self):
        return '({}.{})'.format(self.handle, self.anchor)

    def dumps(self):
        """Return a representation. Alias for consistency."""

        return self.__repr__()


class TikZNode(TikZObject):
    """A class that represents a TiKZ node."""

    _possible_anchors = ['north', 'south', 'east', 'west']

    def __init__(self, handle=None, options=None, at=None, text=None):
        """
        Args
        ----
        handle: str
            Node identifier
        options: list
            List of options
        at: TikZCoordinate
            Coordinate where node is placed
        text: str
            Body text of the node
        """
        super(TikZNode, self).__init__(options=options)

        self.handle = handle

        if isinstance(at, (TikZCoordinate, type(None))):
            self._node_position = at
        else:
            raise TypeError(
                'at parameter must be an object of the'
                'TikzCoordinate class')

        self._node_text = text

    def dumps(self):
        """Return string representation of the node."""

        ret_str = []
        ret_str.append(Command('node', options=self.options).dumps())

        if self.handle is not None:
            ret_str.append('({})'.format(self.handle))

        if self._node_position is not None:
            ret_str.append('at {}'.format(str(self._position)))

        if self._node_text is not None:
            ret_str.append('{{{text}}};'.format(text=self._node_text))
        else:
            ret_str.append('{};')
        return ' '.join(ret_str)

    def get_anchor_point(self, anchor_name):
        """Return an anchor point of the node, if it exists."""

        if anchor_name in self._possible_anchors:
            return TikZNodeAnchor(self.handle, anchor_name)
        else:
            try:
                anchor = int(anchor_name.split('_')[1])
            except:
                anchor = None

            if anchor is not None:
                return TikZNodeAnchor(self.handle, str(anchor))

        raise ValueError('Invalid anchor name: "{}"'.format(anchor_name))

    def __getattr__(self, attr_name):
        try:
            point = self.get_anchor_point(attr_name)
            return point
        except ValueError:
            pass

        # raise AttributeError(
        #    'Invalid attribute requested: "{}"'.format(attr_name))


class TikZUserPath(LatexObject):
    """Represents a possible TikZ path."""

    def __init__(self, path_type, options=None):
        """
        Args
        ----
        path_type: str
            Type of path used
        options: Options
            List of options to add
        """
        super(TikZUserPath, self).__init__()
        self.path_type = path_type
        self.options = options

    def dumps(self):
        """Return path command representation."""

        ret_str = self.path_type

        if self.options is not None:
            ret_str += self.options.dumps()

        return ret_str


class TikZPathList(LatexObject):
    """Represents a path drawing."""

    _base_legal_path_types = ['--', '-|', '|-', 'to',
                         'rectangle', 'circle',
                         'arc', 'edge']



    def __init__(self, *args, additional_path_types=None):
        """
        Args
        ----
        args: list
            A list of path elements
        """
        self._last_item_type = None
        self._arg_list = []

        self._legal_path_types = self._base_legal_path_types
        if additional_path_types is not None:
            self._legal_path_types.extend(additional_path_types)

        # parse list and verify legality
        self._parse_arg_list(args)

    def append(self, item):
        """Add a new element to the current path."""
        self._parse_next_item(item)

    def _parse_next_item(self, item):

        # assume first item is a point
        if self._last_item_type is None:
            try:
                self._add_point(item)
            except (TypeError, ValueError):
                # not a point, do something
                raise TypeError(
                    'First element of path list must be a node identifier'
                    ' or coordinate'
                )
        elif self._last_item_type in ('point', 'arc'):
            # point after point is permitted, doesnt draw

            if isinstance(item, TikZNode):
                # Note that we drop the preceding backslash since that is not part
                # of inline syntax. trailing ";" dropped as well since TikZNode will add this
                self._arg_list.append(item.dumps()[1:-1])
                return
            try:
                self._add_point(item)
                return
            except (ValueError, TypeError):
                # not a point, try path
                pass

            # will raise typeerror if wrong
            self._add_path(item)
        elif self._last_item_type == 'path':
            # only point  or cycle allowed after path
            if isinstance(item, str) and item.strip() == 'cycle':
                self._arg_list.append(item)
                return

            original_exception = None
            try:
                self._add_point(item)
                return
            except (TypeError, ValueError) as ex:
                # check if trying to insert path after path
                try:
                    self._add_path(item, parse_only=True)
                    not_a_path = False
                    original_exception = ex
                except (TypeError, ValueError) as ex:
                    # not a path either!
                    not_a_path = True
                    original_exception = ex

            # disentangle exceptions
            if not_a_path is False:
                raise ValueError('only a point descriptor can come'
                                 ' after a path descriptor')

            if original_exception is not None:
                raise original_exception
        # not path.arc is path specifier "arc", not a TikZArcSpecifier
        elif self._last_item_type == 'path.arc':
            # only allow arc specifier after arc path
            original_exception = None
            try:
                self._add_arc_spec(item)
                return
            except (TypeError, ValueError) as ex:
                raise ValueError('only an arc specifier can come after an '
                                 ' arc path descriptor')

    def _parse_arg_list(self, args):

        for item in args:
            self._parse_next_item(item)

    def _add_path(self, path, parse_only=False):
        if isinstance(path, str):
            if path in self._legal_path_types:
                _path = TikZUserPath(path)
            else:
                raise ValueError('Illegal user path type: "{}"'.format(path))
        elif isinstance(path, TikZUserPath):
            _path = path
        else:
            raise TypeError('Only string or TikZUserPath types are allowed')

        # add
        if parse_only is False:
            self._arg_list.append(_path)
            self._last_item_type = 'path'
            # if arc, need to know since then we expect following to be an arc not a point
            if _path.path_type == "arc":
                self._last_item_type += ".arc"
        else:
            return _path

    def _add_point(self, point, parse_only=False):
        if isinstance(point, str):
            try:
                _item = TikZCoordinate.from_str(point)
            except ValueError:
                raise ValueError('Illegal point string: "{}"'.format(point))
        elif isinstance(point, TikZCoordinate):
            _item = point
        elif isinstance(point, tuple):
            _item = TikZCoordinate(*point)
        elif isinstance(point, TikZNode):
            _item = '({})'.format(point.handle)
        elif isinstance(point, TikZNodeAnchor):
            _item = point.dumps()
        else:
            raise TypeError('Only str, tuple, TikZCoordinate,'
                            'TikZNode or TikZNodeAnchor types are allowed,'
                            ' got: {}'.format(type(point)))
        # add, finally
        if parse_only is False:
            self._arg_list.append(_item)
            self._last_item_type = 'point'
        else:
            return _item

    def _add_arc_spec(self, arc, parse_only=False):
        if isinstance(arc, str):
            try:
                _arc = TikZArcSpecifier.from_str(arc)
            except ValueError:
                raise ValueError('Illegal arc string: "{}"'.format(arc))
        elif isinstance(arc, TikZArcSpecifier):
            _arc = arc
        elif isinstance(arc, tuple):
            _arc = TikZArcSpecifier(*arc)
        # tODO no idea whether node formatting should behave
        elif isinstance(arc, TikZNode):
            _arc = '({})'.format(arc.handle)
        elif isinstance(arc, TikZNodeAnchor):
            _arc = arc.dumps()
        else:
            raise TypeError('Only str, tuple, TikZArcSpecifier,'
                            'TikZNode or TikZNodeAnchor types are allowed,'
                            ' got: {}'.format(type(arc)))
            # add, finally
        if parse_only is False:
            self._arg_list.append(_arc)
            self._last_item_type = 'arc'
        else:
            return _arc

    def dumps(self):
        """Return representation of the path command."""

        ret_str = []
        for item in self._arg_list:
            if isinstance(item, str):
                ret_str.append(item)
            elif isinstance(item, LatexObject):
                ret_str.append(item.dumps())
            else:
                raise TypeError("Dumps failed. Unexpected item type in"
                                "_arg_list")
        return ' '.join(ret_str)



class TikZPath(TikZObject):
    r"""The TikZ \path command."""

    def __init__(self, path=None, options=None):
        """
        Args
        ----
        path: TikZPathList
            A list of the nodes, path types in the path
        options: TikZOptions
            A list of options for the command
        """
        super(TikZPath, self).__init__(options=options)

        additional_path_types = None
        if options is not None and 'use Hobby shortcut' in options:
            additional_path_types = [".."]

        if isinstance(path, TikZPathList):  # if already TikZPathList, should already have been
            # fed arg on construction
            self.path = path
        elif isinstance(path, list):
                self.path = TikZPathList(*path, additional_path_types=additional_path_types)
        elif path is None:
            self.path = TikZPathList(additional_path_types=additional_path_types)
        else:
            raise TypeError(
                'argument "path" can only be of types list or TikZPathList')

    def append(self, element):
        """Append a path element to the current list."""
        self.path.append(element)

    def dumps(self):
        """Return a representation for the command."""

        ret_str = [Command('path', options=self.options).dumps()]

        ret_str.append(self.path.dumps())
        return ' '.join(ret_str) + ';'


class TikZDraw(TikZPath):
    """A draw command is just a path command with the draw option."""

    def __init__(self, path=None, options=None):
        """
        Args
        ----
        path: TikZPathList | List
            A list of the nodes, path types in the path
        options: TikZOptions
            A list of options for the command
        """
        super(TikZDraw, self).__init__(path=path, options=options)

        # append option
        if self.options is not None:
            self.options.append_positional('draw')
        else:
            self.options = TikZOptions('draw')


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
