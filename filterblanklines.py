#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    for line in sys.stdin:
        if len(line.strip()) > 0:
            print(line, end='')
