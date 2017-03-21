#!/usr/bin/env python3
import argparse
import glob
import hashlib
import os
import time
from collections import defaultdict
from functools import partial


def getfilehash(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(partial(f.read, 128 * 1024), b''):
            d.update(buf)
    return d.hexdigest()


def main():
    parser = argparse.ArgumentParser(description='Find files with duplicate hashes')
    parser.add_argument('files', nargs='*', default=glob.glob("*"),
                        help='list of files to check (default: *)')
    args = parser.parse_args()

    hashdict = defaultdict(list)
    for filepath in args.files:
        if not os.path.isfile(filepath):
            continue
        strhash = getfilehash(filepath)
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
                print(f"{columnone}  {time.ctime(os.path.getmtime(filematch))}  {filematch}")

    if firstdupehash:
        print("No duplicates!")


if __name__ == "__main__":
    main()
