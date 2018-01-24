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
    parser.add_argument('paths', nargs='*', default=['.'],
                        help='Folder to search for duplicates (default: .)')
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

    filelist_unfiltered = set()
    for path in args.paths:
        if os.path.isfile(path):
            filelist_unfiltered.add(os.path.normpath(path))
        else:
            filelist_unfiltered.update(
                [os.path.normpath(x) for x in glob.glob(os.path.join(path, '**'), recursive=True)])

    filelist = [x for x in filelist_unfiltered if os.path.isfile(x) and fnmatch.fnmatch(x, args.name)]

    sizedict = {}
    for filepath in filelist:
        sizedict.setdefault(os.path.getsize(filepath), []).append(filepath)

    founddupehash = False
    # loop over file sizes with multiple matches in order of increasing size (because hashing big files is slow)
    for size, filematches in sorted([x for x in sizedict.items() if len(x[1]) > 1], key=lambda x: x[0]):
        if not findconflictmode:
            hashdict_thissize = {}

            for filepath in filematches:
                strhash = getfilehash(filepath)
                hashdict_thissize.setdefault(strhash, []).append(filepath)
                # print(strhash, os.path.getsize(filepath), filepath)

            founddupehashthissize = False
            for strhash, filematches in (x for x in hashdict_thissize.items() if len(x[1]) > 1):
                if founddupehashthissize:
                    print()
                else:
                    if founddupehash:
                        print()
                    print(f"{size} byte files (count {len(filematches)}):")
                founddupehashthissize = True

                for filematch in filematches:
                    mtime = os.path.getmtime(filematch)
                    print(f"  {strhash}  {os.path.getsize(filematch)}  {time.ctime(mtime)}  {filematch}")

            if founddupehashthissize:
                founddupehash = True

        else:

            originalpathhashdict = {}

            for filematch in filematches:
                strhash = getfilehash(filematch)

                suffixpart = "".join(Path(filematch).suffixes)  # contains ".tar.gz" for example
                originalname = Path(filematch).name

                # temporarily remove the suffix part if there is one
                if suffixpart:
                    originalname = originalname[: -len(suffixpart)]

                for dupnum in range(10):
                    endstr = f" ({dupnum:d})"
                    if originalname.endswith(endstr):
                        originalname = originalname[:-len(endstr)]
                originalpath = os.path.normpath(os.path.join(Path(filematch).parent, originalname + suffixpart))

                originalpathhashdict.setdefault((originalpath, strhash), []).append(filematch)

            for (originalpath, strhash), pathhashmatches in (x for x in originalpathhashdict.items() if len(x[1]) > 1):
                if founddupehash:
                    print()

                founddupehash = True

                print(f"'{originalpath}' {strhash}")

                mtimes = [os.path.getmtime(filepath) for filepath in pathhashmatches]
                oldestfilepath = [
                    filepath for filepath in pathhashmatches if os.path.getmtime(filepath) == min(mtimes)][0]

                for filepath in sorted(pathhashmatches):
                    mtime = os.path.getmtime(filepath)

                    keepstr = "  (KEEP)" if filepath == oldestfilepath else ""
                    print(f"   {strhash}, {os.path.getsize(filepath)} bytes, modified {time.ctime(mtime)}, "
                          f"'{filepath}'{keepstr}")
                rmfiles = [filepath for filepath in pathhashmatches if filepath != oldestfilepath]
                for filepath in rmfiles:
                    if dryrun:
                        print(f"   (not executed) rm '{filepath}'")
                    else:
                        print(f"   rm '{filepath}'")
                        os.remove(filepath)
                if oldestfilepath != originalpath:
                    if dryrun:
                        print(f"   (not executed) mv '{oldestfilepath}' '{originalpath}'")
                    else:
                        print(f"   mv '{oldestfilepath}' '{originalpath}'")
                        os.rename(oldestfilepath, originalpath)

    if not founddupehash:
        print(f"No duplicates found among {len(filelist)} files")
    elif findconflictmode and dryrun:
        print("\nThis was a dry run only. Confirm the rename and deletion operations using --confirm")


if __name__ == "__main__":
    main()
