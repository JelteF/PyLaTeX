# -*- coding: utf-8 -*-
"""
    pylatex.PICTURES
    ~~~~~~~

    This module implements the class that deals with graphics.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from .utils import dumps_list
from .base_classes import BaseLaTeXContainer
from .package import Package

from collections import Counter
import re
import pdb


class Graphic(BaseLaTeXContainer):

    """A class that represents a Graphic."""

    def __init__(self, graphName, width = '1', data=None, pos=None, 
                 packages=[Package('graphicx')],placement=r'\centering'):
        """ Width = fraction textwidth"""        
        self.graph_type = 'figure'       
        self.graph_name = graphName
        self.width = width
        self.pos = pos
        self.placement = placement
        super().__init__(data=data, packages=packages)

    def add_label(self, label):
        """Add a label to the figure"""
        self.append(r'\label{'+label+'}')
    def add_caption(self,caption):
        """Add a caption to the figure"""
        self.append(r'\caption{'+caption+'}')


    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        string = r'\begin{' + self.graph_type + '}'
        if self.pos is not None:
            string += '[' + self.pos + ']'
        
        string += '\n'
        if self.placement is not None:
            string += self.placement + '\n'
        string += r'\includegraphics[width='+str(self.width)+r'\textwidth'']'

        self.graph_name
        string += '{' + self._fixGraphName(self.graph_name) + '}'
        
        string += dumps_list(self)

        string += r'\end{' + self.graph_type + '}'+'\n'

        super().dumps()
        return string
        
    def _fixGraphName(self,graphName):
        # Latex has problems if there are one or more points in the filename,
        # thus'abc.def.jpg' will be changed to '{abc.def}.jpg'
        splitName = graphName.split('.')
        newName = '{'+'.'.join(splitName[0:-1])+'}'
        newName = '.'.join([newName,splitName[-1]])
        return(newName)

