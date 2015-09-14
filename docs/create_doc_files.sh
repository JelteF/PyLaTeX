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

LATEX_DOCUMENT_HIDES='dump, dumps_packages, dump_packages, latex_name'
LATEX_OBJECT_MEMBERS="generate_tex $LATEX_DOCUMENT_HIDES"


LATEX_CONTAINER_MEMBERS='create, dumps'


USER_LIST_MEMBERS='append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort'

for rst in source/pylatex/*.rst; do
    if [[ "$rst" != *latex_object.rst ]]; then
        if [[ "$rst" == *containers.rst ]]; then
            echo "    :exclude-members: $LATEX_OBJECT_MEMBERS," \
                "$USER_LIST_MEMBERS" >> $rst
        elif [[ "$rst" == *document.rst ]]; then
            echo "    :exclude-members: $LATEX_DOCUMENT_HIDES," \
                "$USER_LIST_MEMBERS" >> $rst
        else
            echo "    :exclude-members: $LATEX_OBJECT_MEMBERS," \
                "$USER_LIST_MEMBERS, $LATEX_CONTAINER_MEMBERS" >> $rst
        fi
    fi
done

for f in ../examples/*.py; do
    name=`echo $f | cut -d'/' -f3 | cut -d'.' -f1`
    rst=source/examples/${name}.rst
    $python gen_example_title.py "$name" > $rst
    echo Creating file ${rst}
    echo .. automodule:: examples.$name >> $rst
    echo "    :exclude-members: $LATEX_OBJECT_MEMBERS," \
        "$USER_LIST_MEMBERS, $LATEX_CONTAINER_MEMBERS" >> $rst
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
    $python ../../../$f > /dev/null
    for pdf in ${name}*.pdf; do
        convert $pdf ${pdf}.png
        echo ".. figure:: /_static/examples/${pdf}.png" >> ../../../$rst
        echo >> ../../../$rst
        echo "    $pdf" >> ../../../$rst
    done
    rm -f *.pdf *.aux *.tex *.log
    cd ../../..

done
