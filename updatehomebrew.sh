#!/usr/bin/env zsh
set -x #echo on

brew update
brew upgrade
brew upgrade google-drive
brew autoremove
brew cleanup
