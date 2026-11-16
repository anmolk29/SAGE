from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

URL = "https://data.mendeley.com/public-files/datasets/s25x2bnshz/files/ac98aa02-f47d-4049-8497-394a3ba38235/file_downloaded"
OUT = Path("data/provenance/mendeley-conveyor")


def get_range(start: int, end: int) -> bytes:
    req = urllib.request.Request(URL, headers={"Range": f"bytes={start}-{end}", "User-Agent": "SAGE-project-validation/1.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
        if response.status != 206:
            raise RuntimeError(f"Expected HTTP 206 for bytes {start}-{end}, got {response.status}")
        match = re.match(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
        if not match or int(match.group(1)) != start or int(match.group(2)) != end:
            raise RuntimeError(f"Unexpected Content-Range: {response.headers.get('Content-Range')}")
        return data


def central_directory(offset: int, file_size: int) -> tuple[int, int, int]:
    tail_start = max(0, file_size - 65557)
    tail = get_range(tail_start, file_size - 1)
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0:
        raise RuntimeError("ZIP EOCD signature not found in final 65,557 bytes")
    fields = struct.unpack_from("<4s4H2LH", tail, eocd)
    entries = fields[4]
    cd_size = fields[5]
    cd_offset = fields[6]
    if entries != 0xFFFF and cd_size != 0xFFFFFFFF and cd_offset != 0xFFFFFFFF:
        return entries, cd_size, cd_offset

    locator = tail.rfind(b"PK\x06\x07", 0, eocd)
    if locator < 0:
        raise RuntimeError("ZIP64 locator missing")
    zip64_offset = struct.unpack_from("<Q", tail, locator + 8)[0]
    zip64_head = get_range(zip64_offset, zip64_offset + 55)
    z = struct.unpack_from("<4sQ2H2I4Q", zip64_head, 0)
    if z[0] != b"PK\x06\x06":
        raise RuntimeError("ZIP64 EOCD signature invalid")
    entries = z[7]
    cd_size = z[8]
    cd_offset = z[9]
    return entries, cd_size, cd_offset


def parse_extra(extra: bytes, comp: int, uncomp: int, local: int) -> tuple[int, int, int]:
    i = 0
    while i + 4 <= len(extra):
        tag, n = struct.unpack_from("<HH", extra, i)
        val = extra[i + 4:i + 4 + n]
        if tag == 1:
            p = 0
            if uncomp == 0xFFFFFFFF:
                uncomp = struct.unpack_from("<Q", val, p)[0]; p += 8
            if comp == 0xFFFFFFFF:
                comp = struct.unpack_from("<Q", val, p)[0]; p += 8
            if local == 0xFFFFFFFF and p + 8 <= len(val):
                local = struct.unpack_from("<Q", val, p)[0]
            break
        i += 4 + n
    return comp, uncomp, local


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the public Mendeley ZIP central directory using HTTP range requests")
    parser.add_argument("--output-dir", default=OUT.as_posix(), help="directory for the local archive manifest")
    parser.add_argument("--archive-bytes", type=int, default=6_228_464_374, help="archive size reported by the dataset record")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_size = args.archive_bytes
    count, cd_size, cd_offset = central_directory(0, file_size)
    raw = get_range(cd_offset, cd_offset + cd_size - 1)
    entries = []
    i = 0
    while i < len(raw):
        if raw[i:i + 4] != b"PK\x01\x02":
            raise RuntimeError(f"Central-directory signature error at byte {i}")
        v = struct.unpack_from("<4s6H3L5H2L", raw, i)
        comp, uncomp, name_n, extra_n, comment_n = v[8], v[9], v[10], v[11], v[12]
        local = v[16]
        name_start = i + 46
        name = raw[name_start:name_start + name_n].decode("utf-8", errors="replace")
        extra_start = name_start + name_n
        extra = raw[extra_start:extra_start + extra_n]
        comp, uncomp, local = parse_extra(extra, comp, uncomp, local)
        entries.append({
            "path": name,
            "compressed_bytes": comp,
            "uncompressed_bytes": uncomp,
            "compression_method": v[4],
            "crc32": f"{v[7]:08x}",
            "local_header_offset": local,
        })
        i = extra_start + extra_n + comment_n
    if len(entries) != count:
        raise RuntimeError(f"Parsed {len(entries)} ZIP entries, EOCD reports {count}")
    manifest = {"dataset_doi": "10.17632/s25x2bnshz.1", "archive_bytes": file_size,
                "central_directory_entries": count, "entries": entries}
    path = output_dir / "remote_zip_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({
        "archive_bytes": file_size,
        "entry_count": len(entries),
        "central_directory_bytes": cd_size,
        "manifest": str(path),
        "interesting": [e for e in entries if re.search(r"(original-raw-videos|yolo-dataset-center|annotation|label|readme)", e["path"], re.I)],
        "top_level_folders": sorted({e["path"].split("/")[0] for e in entries if "/" in e["path"]}),
    }, indent=2))


if __name__ == "__main__":
    main()
