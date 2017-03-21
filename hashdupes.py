#!/usr/bin/env python3
import os
import glob
from collections import defaultdict
import hashlib
from functools import partial

"""
    Print out all files in the current directory that have duplicate hashes
"""


def hashfile(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(partial(f.read, 128 * 1024), b''):
            d.update(buf)
    return d.hexdigest()


filelist = glob.glob("*", recursive=False)

hashdict = defaultdict(list)
for filepath in filelist:
    if not os.path.isfile(filepath):
        continue
    strhash = hashfile(filepath)
    hashdict[strhash].append(filepath)
    # print(strhash, filepath)

firstdupehash = True
for strhash, filematches in hashdict.items():
    if len(filematches) > 1:
        if not firstdupehash:
            print()
        firstdupehash = False

        for index, filematch in enumerate(filematches):
            columnone = strhash if index == 0 else "".ljust(len(strhash))
            print(f"{columnone}  {filematch}")

if firstdupehash:
    print("No duplicates!")
