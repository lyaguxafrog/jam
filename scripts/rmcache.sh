#!/bin/bash

rm -r .mypy_cache/

find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -exec rm -f {} +
