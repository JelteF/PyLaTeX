#!/usr/bin/env bash
# Optional named arguments:
#      -p COMMAND: the python command that should be used, e.g. -p python3

# Default values
python="python"

# Check if a command line argument was provided as an input argument.
while getopts "p:" opt; do
  case $opt in
    p)
      python=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

ARGS='--separate --force --no-headings --no-toc'

echo Cleaning pylatex and examples
rm -rf source/pylatex/*
rm -rf source/examples/*
rm -rf source/_static/examples/*

sphinx-apidoc -o source/pylatex/ ../pylatex/ $ARGS
echo Removing file source/pylatex/pylatex.rst
rm source/pylatex/pylatex.rst
echo Removing file source/pylatex/pylatex.base_classes.rst
rm source/pylatex/pylatex.base_classes.rst

for f in ../examples/*.py; do
    name=`echo $f | cut -d'/' -f3 | cut -d'.' -f1`
    rst=source/examples/${name}.rst
    $python gen_example_title.py "$name" > $rst
    echo Creating file ${rst}
    echo .. automodule:: examples.$name >> $rst
    echo >> $rst

    echo The code >> $rst
    echo -------- >> $rst
    echo ".. literalinclude:: /../$f" >> $rst
    echo "    :start-after: begin-doc-include" >> $rst
    echo >> $rst

    echo The generated files >> $rst
    echo ------------------- >> $rst
    # Compiling examples to png
    cd source/_static/examples
    $python ../../../$f > /dev/null
    rst=../../../$rst
    for pdf in ${name}*.pdf; do
        convert $pdf ${pdf}.png
        echo ".. literalinclude:: /_static/examples/${pdf%.pdf}.tex" >> $rst
        echo "    :language: latex" >> $rst
        echo "    :linenos:" >> $rst
        echo "    :caption: ${pdf%.pdf}.tex" >> $rst
        echo >> $rst
        echo "$pdf" >> $rst
        echo >> $rst
        for figure in ${pdf}*.png; do
            echo ".. figure:: /_static/examples/${figure}" >> $rst
        done
    done
    rm -f *.pdf *.aux *.log *.fls *.fdb_latexmk
    cd ../../..

done
