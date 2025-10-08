#!/usr/bin/env python3
from pathlib import Path

import compression

import artistools as at


def get_type_escapetype(line: str) -> tuple[str, str]:
    linesplit = line.split()
    type_id = linesplit[2]
    escape_type_id = linesplit[15]
    return type_id, escape_type_id


def main() -> None:
    TYPE_ESCAPE = str(at.packets.type_ids["TYPE_ESCAPE"])
    TYPE_RPKT = str(at.packets.type_ids["TYPE_RPKT"])
    for filein in sorted(Path().glob("packets00_*.out.*")):
        if "parquet" in filein.name:
            continue
        print(f"Inspecting {filein}...", end="")
        linesin = at.zopen(filein).readlines()

        if any(get_type_escapetype(line) != (TYPE_ESCAPE, TYPE_RPKT) for line in linesin if not line.startswith("#")):
            print("contains gamma or non-escaped packets, filtering...")
            backupfolder = filein.parent / "packets_beforefilter"
            backupfolder.mkdir(exist_ok=True)
            fileout_rpkt = Path(
                *filein.parts[:-1],
                filein.parts[-1].removesuffix(".zst").removesuffix(".gz").removesuffix(".xz") + ".zst",
            )
            fileout_rpkt_temp = Path(*fileout_rpkt.parts[:-1], fileout_rpkt.parts[-1] + ".partialtmp")
            print("  writing filtered rpkts..", end="")
            kept_packets = 0

            with compression.zstd.open(fileout_rpkt_temp, "wt", level=12) as foutrpkt:
                for line in linesin:
                    type_id, escape_type_id = get_type_escapetype(line)
                    if line.startswith("#"):
                        assert type_id == "type_id"
                        assert escape_type_id == "escape_type_id"

                        foutrpkt.write(line)
                        continue

                    if type_id == str(at.packets.type_ids["TYPE_ESCAPE"]) and escape_type_id == str(
                        at.packets.type_ids["TYPE_RPKT"]
                    ):
                        foutrpkt.write(line)
                        kept_packets += 1
            size_factor = fileout_rpkt_temp.stat().st_size / filein.stat().st_size
            print(
                f" kept {kept_packets} of {len(linesin)} packets ({kept_packets / len(linesin) * 100:.2f}%) new/old size {size_factor * 100:.2f}%"
            )
            print(f"  Wrote {fileout_rpkt} and backed up {filein} to {backupfolder / filein.name}...")
            filein.rename(backupfolder / filein.name)
            fileout_rpkt_temp.rename(fileout_rpkt)
        else:
            print("contains only escaped rpkts, skipping...")


if __name__ == "__main__":
    main()
