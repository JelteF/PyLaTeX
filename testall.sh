#!/usr/bin/env bash
# This script runs flake8 to test for pep8 compliance and executes all the examples and tests
# run as: testall.sh [-p COMMAND] [clean]
# Optional positional arguments
#      -c: cleans up the latex files generated
# Optional named arguments:
#      -p COMMAND: the python command that should be used, e.g. ./testall.sh -p python3
#

# Default values
python="python"

# Check if a command line argument was provided as an input argument.
while getopts ":p:ch" opt; do
  case $opt in
    p)
      python=$OPTARG
      ;;
    c)
      clean=TRUE
      ;;
    d)
      nodoc=TRUE
      ;;
    h)
      echo This runs all the tests and examples and checks for pep8 compliance
      echo
      echo Options:
      echo '   -c            cleans up the latex and pdf files generated'
      echo '   -p COMMAND    the python command that should be used to run the tests'
      echo "   -d            don't execute the doc tests, they can take long"
      exit 0
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


# Run the examples and tests
python_version=$($python --version |& sed 's|Python \(.\).*|\1|g')

if [ "$python_version" = '3' ]; then
    # Check code guidelines
    echo -e '\e[32mChecking for code style errors \e[0m'
    if ! flake8 pylatex examples tests; then
        exit 1
    fi
fi


if [ "$python_version" = '2' ]; then
    main_folder=python2_source
    cd $main_folder
else
    main_folder=.
fi

echo -e '\e[32mTesting tests directory\e[0m'
if ! nosetests tests/*; then
    exit 1
fi

if [ "$python_version" = '2' ]; then
    cd ..
fi

for f in $main_folder/examples/*.py; do
    echo -e '\e[32mTesting '$f'\e[0m'
    if ! $python $f; then
        exit 1
    fi
done

if [ "$clean" = 'TRUE' ]; then
    rm *.pdf *.log *.aux *.tex
fi


if [ "$python_version" = '3' -a "$nodoc" != 'TRUE' ]; then
    echo -e '\e[32mChecking for errors in docs and docstrings\e[0m'
    cd docs
    ./create_doc_files.sh -p $python
    make clean
    if ! sphinx-build -b html -d build/doctrees/ source build/html -nW; then
        exit 1
    fi
fi
