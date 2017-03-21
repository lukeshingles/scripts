#!/usr/bin/env python3
import argparse
import glob
import hashlib
import os
import time


def getfilehash(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(lambda: f.read(128 * 1024), b''):
            d.update(buf)
    return d.hexdigest()


def main():
    parser = argparse.ArgumentParser(description='Find files with duplicate hashes')
    parser.add_argument('files', nargs='*', default=(x for x in glob.glob("*") if os.path.isfile(x)),
                        help='list of files to check (default: *)')
    args = parser.parse_args()

    filesizecount = {}
    for filepath in args.files:
        size = os.path.getsize(filepath)
        filesizecount[size] = filesizecount.get(size, 0) + 1

    # only hash a file if exist other files with the same file size
    hashdict = {}
    for filepath in (x for x in args.files if filesizecount[os.path.getsize(x)] > 1):
        strhash = getfilehash(filepath)
        hashdict.setdefault(strhash, []).append(filepath)
        # print(strhash, os.path.getsize(filepath), filepath)

    founddupehash = False
    for strhash, filematches in (x for x in hashdict.items() if len(x[1]) > 1):
        if founddupehash:
            print()
        founddupehash = True

        for index, filematch in enumerate(filematches):
            columnone = strhash if index == 0 else "".ljust(len(strhash))
            print(f"{columnone}  {os.path.getsize(filematch)}  {time.ctime(os.path.getmtime(filematch))}  {filematch}")

    if not founddupehash:
        print(f"No duplicates among {len(args.files)} files")


if __name__ == "__main__":
    main()
