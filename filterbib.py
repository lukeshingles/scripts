#!/usr/bin/env python3
from pathlib import Path


def main():
    with (Path("references.bib").open("r") as fin, Path("references_filtered.bib").open("w") as fout):
        waiting_for_closing_brace = False
        for line in fin:
            linestrip = line.strip()
            line_has_closing_brace = linestrip.endswith('},')
            if linestrip.startswith("abstract = ") or linestrip.startswith("file = ") or linestrip.startswith("note = "):
                waiting_for_closing_brace = not line_has_closing_brace
                continue

            if waiting_for_closing_brace:
                if line_has_closing_brace:
                    waiting_for_closing_brace = False
                continue
            else:
                fout.write(line)

if __name__ == "__main__":
    main()
