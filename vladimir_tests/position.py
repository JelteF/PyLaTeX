# -*- coding: utf-8 -*-

import os
import subprocess
import errno
from .base_classes import Environment, Command 
from .package import Package


class Position(Environment):
    #def __init__(self):
        #ragged2e = Package('ragged2e')
        #packages = [ ragged2e ]
        #self.packages |= packages
        #super.__init__()


class Center(Position):


class Flushleft(Position):


class Flushright(Position):
