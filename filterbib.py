#!/usr/bin/env python3
import sys


def main() -> None:
    waiting_for_closing_brace = False
    for line in sys.stdin:
        linestrip = line.strip()
        line_has_closing_brace = linestrip.endswith('},') or linestrip.endswith('}')
        if linestrip.startswith("abstract = ") or linestrip.startswith("file = ") or linestrip.startswith("note = "):
            waiting_for_closing_brace = not line_has_closing_brace
            continue

        if waiting_for_closing_brace:
            if line_has_closing_brace:
                waiting_for_closing_brace = False
            continue
        else:
            print(line, end='')

if __name__ == "__main__":
    main()
