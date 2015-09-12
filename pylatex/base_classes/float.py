# -*- coding: utf-8 -*-
'''
This module implements the classes that deal with floating environments.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
'''

from . import Environment, Command


class Float(Environment):

    '''A class that represents a floating environment.'''

    def __init__(self, position=None, seperate_paragraph=True, **kwargs):
        '''.

        Args
        ----
        position: str
            Define the positioning of a floating environment, for instance
            ``'h'``. See the references for more information.
        seperate_paragraph: bool
            By default floats are positioned inside a separate paragraph.
            Setting this to option to `False` will change that.

        References
        ----------
            * https://www.sharelatex.com/learn/Positioning_of_Figures
        '''

        super().__init__(options=position,
                         seperate_paragraph=seperate_paragraph, **kwargs)

    def add_caption(self, caption):
        '''Add a caption to the float.

        Args
        ----
        caption: str
            The text of the caption.
        '''

        self.append(Command('caption', caption))
