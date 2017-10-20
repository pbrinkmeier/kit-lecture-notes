#!/usr/bin/env python3

"""Table of contents generator for markdown files."""

import sys
import re

# blacklisted headers that will not end up in the toc
blacklist = [
    "table-of-contents",
    "contents",
    "overview"
]

# returns num of hash symbols (= level of header)
def count_hash(line):
    cnt = 0
    for c in line:
        if c == "#":
            cnt += 1
        else:
            return cnt

def convert_link(header):
    # lower case, white spaces are converted to dashes and no characters other
    # than letters and numbers allowed
    link = header.lower().replace(" ", "-")
    return re.sub("[^a-zA-Z0-9\-]", "", link)

# check line for header symbols ('#')
def check_line(line):
    line = line.lstrip().rstrip()
    if not line.startswith("#"):
        return

    # ignore first-level headers
    num = count_hash(line)
    if num < 2:
        return

    title = line[(num + 1):]
    link = convert_link(title)

    if link in blacklist:
        return

    print("    " * (num - 2) + "- ", end='')
    print("[" + title + "](#" + link + ")")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./toc_generator.py <path/to/file.md>")
        sys.exit()

    try:
        with open(sys.argv[1]) as f:
            for l in f:
                check_line(l)
    except IOError:
        print("Cannot find or open file.")
