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
    echo Creating file source/examples/${name}.rst
    echo .. automodule:: $name > source/examples/${name}.rst
done
