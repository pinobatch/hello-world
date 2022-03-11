#!/usr/bin/env python3
"""

File deduplication tool

Copyright 2014, 2020 Damian Yerrick
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

About this program:

There was a complaint in a Cracked article that too many data
deduplication tools on the Internet have severe restrictions
on functionality in the version distributed without charge.
<http://www.cracked.com/photoplasty_529_21-web-browser-features-we-desperately-need/>

This article called to mind a dedupe tool I had written a few
years ago for my private use, so I decided to release it.

To find files with identical contents, drop dedupe.py in a folder
and run it.  It will do the following:

1. Scan all files in all folders and sort them by size.  Reject all
   files with a unique size.
2. Read the first 16K of all remaining files and "hash" each file's
   data by reducing it to a small number using a complicated
   mathematical formula.  Reject all files with a unique hash value.
3. Reread the entire content of all remaining files and hash their
   data.  Reject all files with a unique hash value.
4. Write a list of all duplicate files to the file "dedupe_out.txt".

There is an infinitesimal chance (we're talking 48 zeroes) that two
different files will hash to the same value.  If you find two such
files, you've found a "hash collision", and research universities
will want to hear about it.

Two folders are excluded, so that the tool it can be used on a Linux
home directory without producing irrelevant duplicates:  ~/Desktop.gvfs
folder and any Cache folders inside ~/.mozilla/firefox.

To run this on Windows, you'll need to first install Python from
python.org

Keywords: file duplicate checker free download

Changes

2020-03-17
    port to python 3
2014
    original release

"""
assert str is not bytes
import os
import sys
import hashlib

outfilename = 'dedupe_out.txt'
initial_hash_size = 16384

def sortndrop(dic):
    """Split a mapping to sequence values into lists with len = 1 or > 1

Return a tuple (multis, singles) where
    multis is a list [(k, [v1, v2, ...], ...)]
    singles is a list [(k, v), ...]
"""
    singles = [next(iter(fl)) for (sz, fl) in dic.items() if len(fl) == 1]
    multis = [(sz, fl) for (sz, fl) in dic.items() if len(fl) > 1]
    multis.sort(key=lambda x: -len(x[1]))
    return multis, singles

def minimd5_beginning(filename):
    # 40-bit md5 because this step just narrows the possibilities.
    # Speed is more important than being cryptographically secure
    # for this step.
    h = hashlib.md5()
    with open(filename, 'rb') as infp:
        txt = infp.read(initial_hash_size)
    h.update(txt)
    return h.hexdigest()[:10]

def sha256_entire_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as infp:
        while True:
            txt = infp.read(65536)
            h.update(txt)
            if len(txt) == 0:
                return h.hexdigest()

def add_one_hash(all_files, hash_func):
    same_sets = {}
    c_count = 0
    for (old_key, files) in all_files:
        for filename in sorted(files):
            # extend the key with a new hash, making it
            # more specific
            key = old_key + (hash_func(filename),)
            same_sets.setdefault(key, set())
            same_sets[key].add(filename)
            c_count += 1
            if c_count >= 1000:
                c_count = 1
                sys.stdout.write('M')
                sys.stdout.flush()
    print()
    return sortndrop(same_sets)

def print_stats(step, all_files, singles):
    total_bytes = sum(key[0] * (len(files) - 1)
                      for (key, files) in all_files)
    total_files = sum(len(files) for (key, files) in all_files)
    print("%s drops %d singles\n"
          "leaving %d files in %d dupe groups with %d KiB wasted"
          % (step, len(singles),
             total_files, len(all_files), total_bytes // 1024))

def main():
    print("Reading all folders in %s" % os.getcwd())
    all_files = []
    for (folder, folders, files) in os.walk('.'):
        if "/.mozilla/firefox/" in folder:
            try:
                folders.remove('Cache')
            except ValueError:
                pass
        try:
            folders.remove('.gvfs')
        except ValueError:
            pass
        all_files.extend(os.path.join(folder, filename)
                         for filename in files)

    print("Narrowing to regular files (not symbolic links)")
    all_files = [((),
                  [p for p in all_files if os.path.isfile(p)])]

    print("Starting with %d files" % sum(len(x[1]) for x in all_files))
    all_files, singles = add_one_hash(all_files, os.path.getsize)
    print_stats("Sorting by size", all_files, singles)

    for ((sz,), files) in all_files:
        if sz == 0:
            print("Dropped %d zero-byte files" % len(files))
            files.clear()
    all_files, singles = add_one_hash(all_files, minimd5_beginning)
    print_stats("Hashing first 16 KiB", all_files, singles)

    all_files, singles = add_one_hash(all_files, sha256_entire_file)
    print_stats("Hashing entire file", all_files, singles)

    def all_files_sort_key_func(key):
        ((sz, h1, h2), files) = key
        return -sz * (len(files) - 1)
    all_files.sort(key=all_files_sort_key_func)

    print("Writing to %s" % outfilename)
    with open(outfilename, 'wt') as outfp:
        outfp.write("\n\n".join(repr(h) + "\n" + "\n".join(sorted(files))
                                for (h, files) in all_files))

if __name__=='__main__':
    main()
