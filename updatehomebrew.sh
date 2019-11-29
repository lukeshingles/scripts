#!/usr/bin/env zsh
set -x #echo on

brew update
brew upgrade
brew cask upgrade
brew cleanup
