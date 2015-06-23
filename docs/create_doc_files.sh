#!/bin/bash
ARGS='--separate --force --no-headings --no-toc'

echo Cleaning pylatex and examples
rm -rf source/pylatex/*
rm -rf source/examples/*

sphinx-apidoc -o source/pylatex/ ../pylatex/ $ARGS
echo Removing file source/pylatex/pylatex.rst
rm source/pylatex/pylatex.rst

for f in ../examples/*.py; do
    name=`echo $f | cut -d'/' -f3 | cut -d'.' -f1`
    rst=source/examples/${name}.rst
    echo Creating file ${rst}
    echo .. automodule:: $name > $rst
    echo >> $rst
    echo ".. literalinclude:: /../$f" >> $rst
    echo "    :start-after: begin-doc-include" >> $rst

done
