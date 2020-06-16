#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo ERROR: Please supply the version number
    exit 1
fi

if [[ "$1" != v* ]]; then
    echo ERROR: The version number should start with a v
    exit 1
fi

if [[ -n $(git status --porcelain) ]]; then
    echo "ERROR: repo is dirty, please commit everything"
    exit 1
fi

if ! grep "$1" docs/source/changelog.rst > /dev/null; then
    echo "ERROR: You forgot to update the changelog"
    exit 1
fi

./testall.sh

set -x

git tag "$1" -a -m ''

./convert_to_py2.sh

cd docs
./create_doc_files.sh
make clean
make html
cd gh-pages
git add -A
git commit -m "Updating docs to version $1"

while true; do
    read -rp "Going to irreversibly release stuff now as $1. Are you sure y/n?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

git push

git submodule add --force ../PyLaTeX.git "version_submodules/$1"
cd version_submodules/"$1"
git checkout gh-pages
git pull
cd ../../

ln -s "version_submodules/$1/latest/" "$1"
rm current
ln -s "$1" current
git add -A
git commit -m "Updated symlinks for version $1"

while true; do
    read -rp "Going to irreversibly release stuff now as $1. Are you sure y/n?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done


git push

cd ../..

git push
git push --tags
python setup.py sdist upload
