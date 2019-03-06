# -*- coding: utf-8 -*-
"""This module implements the label command and reference."""

from .base_classes import CommandBase
from .package import Package
from .base_classes import LatexObject


def _remove_invalid_char(s):
    """Remove invalid and dangerous characters from a string."""

    s = ''.join([i if ord(i) >= 32 and ord(i) < 127 else '' for i in s])
    s = s.translate(dict.fromkeys(map(ord, "_%~#\\{}\":")))
    return s


def make_label(label, prefix="", default_name=None):
    """
    Helper function for generating a `Label` object from arguments that are passed to a LatexObjects
    __init__ function. Will create a corresponding `Marker` if necessary.
    Args
    ----
    label: Label or bool or str or Marker
        The label parameter. Can be a string, in which case a `Marker` will be built. If the string contains a colon,
        the it is split into prefix and name. If `label` is a boolean, and `default_name` is set, this name will be used
        as the label's name.
    prefix: str
        The prefix to use if `label` is a string that does not contain a colon.
    default_name: str
        The label name to use if `label` is `True`.
    Returns
    -------
    Label

    """
    if isinstance(label, Label):
        return label
    elif isinstance(label, Marker):
        return Label(label)
    elif isinstance(label, str):
        if ':' in label:
            label = label.split(':', 1)
            return Label(Marker(label[1], label[0]))
        else:
            return Label(Marker(label, prefix))
    elif label is True:
        if default_name is None:
            raise ValueError("No label name given")
        return Label(Marker(default_name, prefix))
    elif label is False or label is None:
        return None
    else:
        raise TypeError("Unexpected type %s for label" % type(label))


class Marker(LatexObject):
    """A class that represents a marker (label/ref parameter)."""

    _repr_attributes_override = [
        'name',
        'prefix',
    ]

    def __init__(self, name, prefix="", del_invalid_char=True):
        """
        Args
        ----
        name: str
            Name of the marker.
        prefix: str
            Prefix to add before the name (prefix:name).
        del_invalid_char: bool
            If True invalid and dangerous characters will be
            removed from the marker
        """

        if del_invalid_char:
            prefix = _remove_invalid_char(prefix)
            name = _remove_invalid_char(name)
        self.prefix = prefix
        self.name = name

    def __str__(self):
        return ((self.prefix + ":") if self.prefix != "" else "") + self.name

    def dumps(self):
        """Represent the Marker as a string in LaTeX syntax.

        Returns
        -------
        str

        """
        return str(self)


class RefLabelBase(CommandBase):
    """A class used as base for command that take a marker only."""

    _repr_attributes_mapping = {
        'marker': 'arguments',
    }

    def __init__(self, marker):
        """
        Args
        ----
        marker: Marker
            The marker to use with the label/ref.
        """

        self.marker = marker
        super().__init__(arguments=(str(marker)))


class Label(RefLabelBase):
    """A class that represents a label."""


class Ref(RefLabelBase):
    """A class that represents a reference."""


class Pageref(RefLabelBase):
    """A class that represents a page reference."""


class Eqref(RefLabelBase):
    """A class that represent a ref to a formulae."""

    packages = [Package('amsmath')]


class Cref(RefLabelBase):
    """A class that represent a cref (not a Cref)."""

    packages = [Package('cleveref')]


class CrefUp(RefLabelBase):
    """A class that represent a Cref."""

    packages = [Package('cleveref')]
    latex_name = 'Cref'


class Autoref(RefLabelBase):
    """A class that represent an autoref."""

    packages = [Package('hyperref')]


class Hyperref(CommandBase):
    """A class that represents an hyperlink to a label."""

    _repr_attributes_mapping = {
        'marker': 'options',
        'text': 'arguments',
    }

    packages = [Package('hyperref')]

    def __init__(self, marker, text):
        """
        Args
        ----
        marker: Marker
            The marker to use with the label/ref.
        text: str
            The text that will be shown as a link
            to the label of the same marker.
        """

        self.marker = marker
        super().__init__(options=(str(marker)), arguments=text)
