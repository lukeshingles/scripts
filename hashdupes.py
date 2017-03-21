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
    parser.add_argument('files', nargs='*', default=glob.glob("*"),
                        help='list of files to check (default: *)')
    args = parser.parse_args()

    filelist = [x for x in args.files if os.path.isfile(x)]

    sizedict = {}
    for filepath in filelist:
        sizedict.setdefault(os.path.getsize(filepath), []).append(filepath)

    founddupehash = False
    # loop over file sizes with multiple matches in order of increasing size (because hasing big files is hash)
    for size, filematches in sorted([x for x in sizedict.items() if len(x[1]) > 1], key=lambda x: x[0]):
        hashdict = {}

        for filepath in filematches:
            strhash = getfilehash(filepath)
            hashdict.setdefault(strhash, []).append(filepath)
            # print(strhash, os.path.getsize(filepath), filepath)

        founddupehashthissize = False
        for strhash, filematches in (x for x in hashdict.items() if len(x[1]) > 1):
            if founddupehashthissize:
                print()
            else:
                if founddupehash:
                    print()
                print(f"{size} byte files:")
            founddupehashthissize = True

            for index, filematch in enumerate(filematches):
                columnone = strhash  # if index == 0 else "".ljust(len(strhash))
                print(f"  {columnone}  {os.path.getsize(filematch)}  "
                      f"{time.ctime(os.path.getmtime(filematch))}  {filematch}")

        if founddupehashthissize:
            founddupehash = True

    if not founddupehash:
        print(f"No duplicates among {len(filelist)} files")


if __name__ == "__main__":
    main()
