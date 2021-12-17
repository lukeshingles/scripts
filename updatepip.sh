#!/usr/bin/env zsh
# set -x #echo on

declare -a arr=("pypy3" "python3.10")

# now loop through the above array
for pyver in "${arr[@]}"
do
   $pyver -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 $pyver -m pip install --upgrade
done
