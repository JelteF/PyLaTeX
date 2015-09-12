#!/bin/bash

# This is used to convert the python3 code to python2 compatible code. It needs
# 3to2 to actually work correctly.

mkdir -p python2_source
cp -R pylatex tests examples python2_source
3to2 python2_source -wn --no-diffs -f collections -f all
