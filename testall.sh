#!/usr/bin/env bash

for f in {tests,examples}/*.py; do
    echo -e '\e[32mTesting '$f'\e[0m'
    if ! python $f; then
        exit 1
    fi
done
