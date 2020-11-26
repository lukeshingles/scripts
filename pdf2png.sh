#!/usr/bin/env zsh

for file in "$@"
do
    newfile=$(basename "$file" .pdf).png
    sips -s format png "$file" --out "$newfile"
done