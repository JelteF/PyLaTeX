#!/usr/bin/env bash

# Check code guidelines
echo -e '\e[32mChecking for code style errors \e[0m'
if ! flake8 pylatex examples tests; then
    exit 1
fi

python_version=$(python --version |& sed 's|Python \(.\).*|\1|g')

if [ "$python_version" = '2' ]; then
    main_folder=python2_source
else
    main_folder=.
fi

for f in $main_folder/{tests,examples}/*.py; do
    echo -e '\e[32mTesting '$f'\e[0m'
    if ! python $f; then
        exit 1
    fi
done

if [ "$1" = 'clean' ]; then
    rm *.pdf *.log *.aux *.tex
fi
