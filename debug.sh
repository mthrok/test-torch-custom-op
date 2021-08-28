#!/usr/bin/env bash

python setup.py develop

export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:$(pwd)/foo"
python -c 'import foo'
