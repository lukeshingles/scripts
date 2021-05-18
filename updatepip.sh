#!/usr/bin/env zsh
set -x #echo on

declare -a arr=("python3.8" "python3.9" "python3.10" "pypy3")

## now loop through the above array
for pyver in "${arr[@]}"
do
   $pyver -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 $pyver -m pip install --upgrade
done


#python3 -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 python3 -m pip install --upgrade
