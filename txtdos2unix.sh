#!/usr/bin/env zsh

if [ $# -eq 0 ]; then
  echo 1>&2 "Usage: $0 [file ...]"
  exit 3
fi

for file in "$@"
do
  if [[ -f "$file" ]]; then
    vim $file -c "set ff=unix" -c ":wq"
  else
    echo File "$file" does not exist
  fi
done