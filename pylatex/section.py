# -*- coding: utf-8 -*-
'''
This module implements the section type classes.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
'''


from .base_classes import SectionBase


class Section(SectionBase):

    '''A class that represents a section.'''


class Subsection(SectionBase):

    '''A class that represents a subsection.'''


class Subsubsection(SectionBase):

    '''A class that represents a subsubsection.'''
