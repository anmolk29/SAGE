# Dataset audit helpers

These scripts inspect the public Mendeley ZIP metadata and selectively retrieve checked archive members without downloading the full archive.

- `inspect_remote_zip.py` reads the remote central directory and writes `data/provenance/mendeley-conveyor/remote_zip_manifest.json`.
- `extract_remote_subset.py` extracts one source video plus a consecutive range of numbered JPEGs. It verifies each member's uncompressed size and ZIP CRC and writes a receipt beside the extracted files.

Run from the project root. Both commands require network access to the public Mendeley record. The full archive is approximately 6.23 GB; the scripts use range requests, but the default subset extractor still retrieves one full MP4 in addition to its selected JPEGs. The selected clip subsets and provenance checks used in this study are already present locally.
