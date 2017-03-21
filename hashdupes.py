#!/usr/bin/env python3
import sys
from collections import defaultdict

"""
    Example usages: shasum * | hashdupes.py
"""

hashdict = defaultdict(list)
for line in sys.stdin:
    hashendpos = line.index(' ')
    strhash, filename = line[:hashendpos], line[hashendpos + 2:].rstrip('\n')
    hashdict[strhash].append(filename)

firstdupehash = True
for strhash, filematches in hashdict.items():
    if len(filematches) > 1:
        if not firstdupehash:
            print()
        firstdupehash = False

        for index, filematch in enumerate(filematches):
            columnone = strhash if index == 0 else "".ljust(len(strhash))
            print(f"{columnone}  {filematch}")
