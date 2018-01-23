#!/usr/bin/env python3
import argparse
import fnmatch
import glob
import hashlib
import os
import time

from pathlib import Path


def getfilehash(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(lambda: f.read(128 * 1024), b''):
            d.update(buf)
    return d.hexdigest()


def main():
    parser = argparse.ArgumentParser(description='Find files with duplicate hashes')
    parser.add_argument('files', nargs='*', default=glob.glob("**", recursive=True),
                        help='list of files to check (default: *)')
    parser.add_argument('-name', default='*',
                        help='Pattern to match filenames (default: *)')
    parser.add_argument('--cloudconflicts', default=False, action='store_true',
                        help=(
                            'Find Google Drive/OneDrive conflict duplicates '
                            '[file.txt, file (1).txt, file(2).txt] with matching hashes'
                            ' and select the earliest-modified file.'))
    parser.add_argument('--confirm', default=False, action='store_true',
                        help='Execute the delete and rename commands suggested by --findconflicts')
    args = parser.parse_args()

    findconflictmode = args.cloudconflicts
    dryrun = not args.confirm

    filelist = [x for x in args.files if os.path.isfile(x) and fnmatch.fnmatch(x, args.name)]

    sizedict = {}
    for filepath in filelist:
        sizedict.setdefault(os.path.getsize(filepath), []).append(filepath)

    founddupehash = False
    # loop over file sizes with multiple matches in order of increasing size (because hashing big files is slow)
    for size, filematches in sorted([x for x in sizedict.items() if len(x[1]) > 1], key=lambda x: x[0]):
        hashdict = {}

        for filepath in filematches:
            strhash = getfilehash(filepath)
            hashdict.setdefault(strhash, []).append(filepath)
            # print(strhash, os.path.getsize(filepath), filepath)

        founddupehashthissize = False
        for strhash, filematches in (x for x in hashdict.items() if len(x[1]) > 1):
            if not findconflictmode:
                if founddupehashthissize:
                    print()
                else:
                    if founddupehash:
                        print()
                    print(f"{size} byte files:")
                founddupehashthissize = True

            fileconflicts = {}
            for index, filematch in enumerate(filematches):
                mtime = os.path.getmtime(filematch)

                if findconflictmode:
                    suffixpart = "".join(Path(filematch).suffixes)  # contains ".tar.gz" for example
                    originalname = Path(filematch).name

                    # temporarily remove the suffix part if there is one
                    if suffixpart:
                        originalname = originalname[: -len(suffixpart)]

                    for dupnum in range(10):
                        endstr = f" ({dupnum:d})"
                        if originalname.endswith(endstr):
                            originalname = originalname[:-len(endstr)]
                    originalpath = os.path.join(Path(filematch).parent, originalname + suffixpart)
                    # fileconflictsets

                    if originalpath not in fileconflicts:
                        fileconflicts[originalpath] = []
                    fileconflicts[originalpath].append(filematch)
                else:
                    print(f"  {strhash}  {os.path.getsize(filematch)}  {time.ctime(mtime)}  {filematch}")

            if findconflictmode:
                for originalpath, filepaths in fileconflicts.items():
                    if len(filepaths) > 1:
                        if founddupehash:
                            print()
                        print(f"{originalpath}")

                        mtimes = [os.path.getmtime(filepath) for filepath in filepaths]

                        oldestfilepath = [
                            filepath for filepath in filepaths if os.path.getmtime(filepath) == min(mtimes)][0]

                        for filepath, mtime in zip(filepaths, mtimes):
                            keepstr = "  (KEEP)" if filepath == oldestfilepath else ""
                            print(f"   {strhash}, {os.path.getsize(filepath)} bytes, modified {time.ctime(mtime)}, "
                                  f"'{filepath}'{keepstr}")
                        print()
                        rmfiles = [filepath for filepath in filepaths if filepath != oldestfilepath]
                        for filepath in rmfiles:
                            if dryrun:
                                print(f"   (not executed) rm '{filepath}'")
                            else:
                                print(f"   rm '{filepath}'")
                                os.remove(filepath)
                        if dryrun:
                            print(f"   (not executed) mv '{oldestfilepath}' '{originalpath}'")
                        else:
                            print(f"   mv '{oldestfilepath}' '{originalpath}'")
                            os.rename(oldestfilepath, originalpath)
                        founddupehash = True

        if founddupehashthissize:
            founddupehash = True

    if not founddupehash:
        print(f"No duplicates found among {len(filelist)} files")
    elif findconflictmode and dryrun:
        print("\nThis was a dry run only. Confirm the rename and deletion operations using --confirm")


if __name__ == "__main__":
    main()
