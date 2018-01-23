#!/usr/bin/env bash
set -x #echo on
#mr -j 4 update
updatehomebrew.sh
updatepip.sh

#tlmgr update --self --all
#--reinstall-forcibly-removed