#!/bin/bash

git clone --branch=gh-pages `git config --get remote.origin.url` gh-pages
rm -rf build/html
ln -sf ../gh-pages/latest build/html
