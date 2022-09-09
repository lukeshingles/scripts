#!/usr/bin/env zsh
# set -x #echo on

#declare -a arr=("python3.9" "python3.10")

declare -a arr=("python3.10" "python3.11")

# now loop through the above array
for pyver in "${arr[@]}"
do
   $pyver -m pip list --format=freeze --outdated | cut -d '=' -f1 | xargs -n1 $pyver -m pip install --use-deprecated legacy-resolver --upgrade
done
