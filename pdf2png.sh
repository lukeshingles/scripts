#!/usr/bin/env zsh

if [ $# -eq 0 ]; then
  echo 1>&2 "Usage: $0 [file ...]"
  exit 3
fi

for file in "$@"
do
    newfile=${file%.pdf}.png
    sips -s format png "$file" --resampleWidth 1024 --out "$newfile"
done
