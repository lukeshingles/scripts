#!/usr/bin/env bash
set -x #echo on

#pip2 list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 pip2 install -U
pip3 list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 pip3 install --user -U
