#!/bin/sh
DATESTR="$(date -u +%Y%m%dT%H%MZ)"
find . -type f -not -name "checksums*.sha256.txt" -print0|xargs -0 shasum -a 256 > checksums-${DATESTR}.sha256.txt

#alternatively openssl md5
