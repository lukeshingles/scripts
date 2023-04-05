#!/usr/bin/env zsh
set -u
lz4cat "$@" | less