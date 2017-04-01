#!/usr/bin/env bash
set -x #echo on
updatehomebrew.sh
updatepip.sh
tlmgr update --self --all --reinstall-forcibly-removed