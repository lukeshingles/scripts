#!/usr/bin/env bash
set -x #echo on

brew update
brew upgrade
brew cleanup
brew cask upgrade
brew cask cleanup