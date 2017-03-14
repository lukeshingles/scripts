#!/usr/bin/env bash

pip2 list --outdated | cut -d ' ' -f1 | xargs -n1 pip2 install -U
pip3 list --outdated | cut -d ' ' -f1 | xargs -n1 pip3 install -U