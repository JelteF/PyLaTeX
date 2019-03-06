# -*- coding: utf-8 -*-
"""
This module implements the classes that deal with floating environments.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
from ..labelref import make_label
from . import Environment, Command


class Float(Environment):
    """A class that represents a floating environment."""

    #: Default prefix to use with Marker
    marker_prefix = "float"

    #: By default floats are positioned inside a separate paragraph.
    #: Setting this to option to `False` will change that.
    separate_paragraph = True

    _repr_attributes_mapping = {
        'position': 'options',
    }

    def __init__(self, *, position=None, **kwargs):
        """
        Args
        ----
        position: str
            Define the positioning of a floating environment, for instance
            ``'h'``. See the references for more information.

        References
        ----------
            * https://www.sharelatex.com/learn/Positioning_of_Figures
        """

        super().__init__(options=position, **kwargs)

    def add_caption(self, caption, label=None):
        """Add a caption to the float.

        Args
        ----
        caption: str
            The text of the caption.
        label: Label or Marker or str
            The label to use for this float.
        Returns
        -------
        Marker
            If a label has been created, its `~.Marker` is returned.
        """

        self.append(Command('caption', caption))
        label = make_label(label, self.marker_prefix)
        if label is not None:
            self.append(label)
            return label.marker

        return None
