#!/usr/bin/env zsh
set -x #echo on

python3 -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 python3 -m pip install --upgrade
