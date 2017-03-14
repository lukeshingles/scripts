#!/bin/sh
FILESTR="$(ls -1 checksums-*.sha256.txt | tail -1)"
echo ${FILESTR}
shasum -c ${FILESTR}

#alternatively openssl md5
