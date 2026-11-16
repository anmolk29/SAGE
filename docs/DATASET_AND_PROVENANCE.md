# Dataset and provenance

## Current pilot

The completed public-data pilot uses three selected clips from the Mendeley dataset *Image Dataset for Foreign Object Detection in Iron Ore Conveyor Belt Systems* (dataset DOI [10.17632/s25x2bnshz.1](https://doi.org/10.17632/s25x2bnshz.1)). The dataset record displays CC BY 4.0. Retain attribution and review third-party content before redistribution.

The frame labels come from manual-split folder membership and are weak/manual. Dataset-wide label reliability and inter-annotator agreement have not been independently established. The selected clips and interval construction support descriptive pilot results only.

The sensor-cue simulator derives event starts from those same annotations. Sensor-guided results are therefore oracle-derived simulations, not independent sensor evidence. No physical sensors, edge-device performance, or energy measurements are included.

## Validation evidence

See [dataset validation](research/DATASET_VALIDATION.md) for archive inspection, source-frame correspondence checks, the selected clips, and remaining annotation/rights limits. See [public-data pilot](research/PUBLIC_DATA_PILOT.md) for run configuration and results. Checksum evidence for selected frames is in `research/evidence/manual_split_provenance_check.json`.

IPAD was considered but not used because dataset-specific reuse rights, temporal metadata, and annotation reliability were not sufficiently verified for this study. It remains a candidate for future work, not the dataset used in the reported pilot.

## Local data and repository policy

Raw archives, extracted frames, derived clips, and per-run result folders are kept in local `data/` and `results/` directories and are excluded from Git. The repository includes the experiment code, documentation, compact model-evaluation records, and the pretrained ResNet-18 file with its license and checksum in `models/pretrained/README.md`.
