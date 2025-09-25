#!/bin/zsh
set -x #echo on

pyver=("python3")
#pyver=("python3.12" "python3.13")

for i in {1..$#pyver}; do

    ${pyver[i]} -m uv pip list --outdated --exclude-editable --exclude artistools --exclude pynonthermal | tee /dev/tty | tail -n +3 | cut -w -f1 | xargs -n1 ${pyver[i]} -m uv pip install --upgrade

done

uv pip install --upgrade --pre ty
