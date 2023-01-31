#!/usr/bin/env zsh
# set -x #echo on

#declare -a arr=("python3.9" "python3.10")

# declare -a arr=("python3.10" "python3.11")
declare -a arr=("python3.11")

#--use-deprecated legacy-resolver

# now loop through the above array
#$pyver -m pip install --upgrade
for pyver in "${arr[@]}"
do
    $pyver -m pip list freeze --outdated | tail -n +3 | cut -w -f1 | xargs -n1 $pyver -m pip install --upgrade
done
