#!/bin/bash

set -e

# python3 또는 python 명령어를 찾습니다.
PYTHON=$(command -v python3 || command -v python)
PIP="$PYTHON -m pip"

$PIP install --upgrade pip
$PIP install pre-commit
$PIP install black
$PIP install flake8
