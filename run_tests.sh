#!/bin/bash

# cd to the current file's dir
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# name of the virtual environment
VENVNAME="myenv"

if [ ! -d "$VENVNAME" ]; then
    python -m venv $VENVNAME
fi

source "$VENVNAME/bin/activate"

pip install -r requirements.txt

# run tests
python -m pytest -v
