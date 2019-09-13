#!/usr/bin/env bash
set -x #echo on

#pip2 list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 pip2 install -U
python3 -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 python3 -m pip install --user -U
