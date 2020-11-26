#!/usr/bin/env zsh
set -x #echo on

python3 -m pip list --use-feature=2020-resolver --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 python3 -m pip install --use-feature=2020-resolver -U
