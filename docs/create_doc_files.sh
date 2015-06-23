#!/bin/bash
ARGS='--separate --force --no-headings --no-toc'

echo Cleaning pylatex and examples
rm -rf source/pylatex/*
rm -rf source/examples/*
rm -rf source/_static/examples/*

sphinx-apidoc -o source/pylatex/ ../pylatex/ $ARGS
echo Removing file source/pylatex/pylatex.rst
rm source/pylatex/pylatex.rst

for f in ../examples/*.py; do
    name=`echo $f | cut -d'/' -f3 | cut -d'.' -f1`
    rst=source/examples/${name}.rst
    python gen_example_title.py "$name" > $rst
    echo Creating file ${rst}
    echo .. automodule:: $name >> $rst
    echo >> $rst

    echo The code >> $rst
    echo -------- >> $rst
    echo ".. literalinclude:: /../$f" >> $rst
    echo "    :start-after: begin-doc-include" >> $rst
    echo >> $rst

    echo The generated pdfs >> $rst
    echo ------------------ >> $rst
    # Compiling examples to png
    cd source/_static/examples
    python ../../../$f > /dev/null
    for pdf in ${name}*.pdf; do
        convert $pdf ${pdf}.png
        echo ".. figure:: /_static/examples/${pdf}.png" >> ../../../$rst
        echo >> ../../../$rst
        echo "    $pdf" >> ../../../$rst
    done
    rm -f *.pdf *.aux *.tex *.log
    cd ../../..

done
