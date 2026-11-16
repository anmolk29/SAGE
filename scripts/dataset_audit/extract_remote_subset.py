from __future__ import annotations

import json
import argparse
import os
import struct
import urllib.request
import zlib
from pathlib import Path, PurePosixPath

URL = "https://data.mendeley.com/public-files/datasets/s25x2bnshz/files/ac98aa02-f47d-4049-8497-394a3ba38235/file_downloaded"
MANIFEST = Path("data/provenance/mendeley-conveyor/remote_zip_manifest.json")
DEST_ROOT = Path("data/raw/mendeley-conveyor")
DEFAULT_STEM = "boardcamera_iron_ore_7_wood_2"
DEFAULT_FIRST_ID = 2106
DEFAULT_LAST_ID = 2455


def get_range(start: int, end: int) -> bytes:
    req = urllib.request.Request(URL, headers={"Range": f"bytes={start}-{end}", "User-Agent": "SAGE-project-validation/1.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as response:
        data = response.read()
        if response.status != 206:
            raise RuntimeError(f"Expected HTTP 206, got {response.status}")
        if len(data) != end - start + 1:
            raise RuntimeError(f"Wrong payload length for bytes {start}-{end}: {len(data)}")
        return data


def payload_start(entry: dict) -> int:
    head = get_range(entry["local_header_offset"], entry["local_header_offset"] + 29)
    fields = struct.unpack("<4s5H3I2H", head)
    if fields[0] != b"PK\x03\x04":
        raise RuntimeError(f"Invalid local file header for {entry['path']}")
    return entry["local_header_offset"] + 30 + fields[9] + fields[10]


def inflate(entry: dict, chunk: bytes, rel: int) -> bytes:
    comp_size = entry["compressed_bytes"]
    method = entry["compression_method"]
    if method == 0:
        data = chunk[rel:rel + comp_size]
    elif method == 8:
        data = zlib.decompress(chunk[rel:rel + comp_size], -15)
    else:
        raise RuntimeError(f"Unsupported ZIP method {method} for {entry['path']}")
    crc = zlib.crc32(data) & 0xFFFFFFFF
    if crc != int(entry["crc32"], 16):
        raise RuntimeError(f"CRC mismatch for {entry['path']}")
    if len(data) != entry["uncompressed_bytes"]:
        raise RuntimeError(f"Uncompressed size mismatch for {entry['path']}")
    return data


def save_entries(entries: list[dict], target_for_path) -> list[dict]:
    # Cluster central-directory members by archive offset. One ranged read per
    # cluster includes the local headers and payloads; this avoids hundreds
    # of network round trips while keeping the far-away raw-video member apart.
    ordered = sorted(entries, key=lambda e: e["local_header_offset"])
    groups: list[list[dict]] = []
    for e in ordered:
        estimated_end = e["local_header_offset"] + 30 + len(e["path"].encode("utf-8")) + e["compressed_bytes"] + 8192
        if not groups or e["local_header_offset"] - groups[-1][-1]["_estimated_end"] > 2_000_000:
            groups.append([])
        e["_estimated_end"] = estimated_end
        groups[-1].append(e)
    records = []
    for group in groups:
        block_start = group[0]["local_header_offset"]
        block_end = max(e["_estimated_end"] for e in group) - 1
        block = get_range(block_start, block_end)
        for e in group:
            header_rel = e["local_header_offset"] - block_start
            fields = struct.unpack_from("<4s5H3I2H", block, header_rel)
            if fields[0] != b"PK\x03\x04":
                raise RuntimeError(f"Invalid local file header for {e['path']}")
            start = e["local_header_offset"] + 30 + fields[9] + fields[10]
            out = target_for_path(e["path"])
            out.parent.mkdir(parents=True, exist_ok=True)
            data = inflate(e, block, start - block_start)
            out.write_bytes(data)
            records.append({"archive_path": e["path"], "local_path": str(out), "bytes": len(data), "crc32": e["crc32"]})
            e.pop("_estimated_end", None)
    return records


def safe_target(archive_path: str, dest: Path) -> Path:
    parts = PurePosixPath(archive_path).parts
    if any(p in ("..", "") for p in parts):
        raise RuntimeError(f"Unsafe archive path: {archive_path}")
    return dest.joinpath(*parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a small, CRC-checked subset from the Mendeley SAGE dataset archive")
    parser.add_argument("--stem", default=DEFAULT_STEM)
    parser.add_argument("--first-id", type=int, default=DEFAULT_FIRST_ID)
    parser.add_argument("--last-id", type=int, default=DEFAULT_LAST_ID)
    args = parser.parse_args()
    if args.first_id > args.last_id:
        parser.error("--first-id must not exceed --last-id")
    stem, first_id, last_id = args.stem, args.first_id, args.last_id
    dest = DEST_ROOT / stem
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_name = {e["path"]: e for e in manifest["entries"]}
    selected = [by_name[f"original-raw-videos/{stem}.mp4"]]
    selected.extend(by_name[f"image-files/{stem}/{i}-{stem}.jpeg"] for i in range(first_id, last_id + 1))
    records = save_entries(selected, lambda path: safe_target(path, dest))
    receipt = {
        "dataset": "In-lab Image Dataset of Foreign Objects and Anomalies in Iron Ore Conveyor Belts",
        "dataset_doi": "10.17632/s25x2bnshz.1",
        "dataset_license": "CC BY 4.0",
        "archive_bytes": manifest["archive_bytes"],
        "dataset_archive_sha256_mendeley_record": "f4ced924f274bcd729fd77ab0aca8fa72a48b5419077e2862b87ab175fd12480",
        "mendeley_file_name": "image-data.zip",
        "mendeley_file_id": "ac98aa02-f47d-4049-8497-394a3ba38235",
        "archive_checksum_source": "Mendeley public file-list metadata; full archive was not downloaded locally.",
        "dataset_record_url": "https://data.mendeley.com/datasets/s25x2bnshz/1",
        "retrieved_at_utc": "2026-11-16",
        "source_video": f"original-raw-videos/{stem}.mp4",
        "sampled_frames": [first_id, last_id],
        "files": records,
    }
    receipt_path = dest / "subset_provenance.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"files_extracted": len(records), "total_bytes": sum(r["bytes"] for r in records), "provenance": str(receipt_path)}, indent=2))


if __name__ == "__main__":
    main()
