# Dataset validation and provenance

**Updated:** 16 November 2026. `sources/` remains untouched. A bounded public-data pilot now evaluates three selected labeled transitions in the Mendeley iron-ore conveyor dataset. It remains an exploratory weak-label evaluation, not a dataset-wide benchmark.

## IPAD decision

IPAD remains the stronger topic match for broad industrial video anomaly detection, but it is not used in this run. Its paper is peer reviewed in *IEEE Transactions on Circuits and Systems for Video Technology*, 35(1), 380–393 (2025), DOI 10.1109/TCSVT.2024.3465517. The official project page and the secondary Hugging Face mirror did not establish dataset-specific reuse terms, validated source timestamps, or annotation reliability. The Elsevier October 2026 source list verifies that TCSVT was covered by Scopus for 2025; this is source/year coverage, not confirmation that this exact DOI record appears in Scopus. No IPAD archive is stored locally.

## Mendeley conveyor dataset audit

The [Mendeley record](https://data.mendeley.com/datasets/s25x2bnshz/1) lists the dataset as CC BY 4.0, DOI 10.17632/s25x2bnshz.1. Its archive is 6,228,464,374 bytes with SHA-256 `f4ced924f274bcd729fd77ab0aca8fa72a48b5419077e2862b87ab175fd12480`. The archive was inspected through HTTP range reads; the full archive was not downloaded. A selective subset was retrieved, and each extracted ZIP member passed uncompressed-size and CRC checks.

Archive inventory found 69,677 members, including 19 raw MP4s, extracted image sequences, sparse manual normal/anomaly folders (the source spells the folder `annomaly`), and YOLO splits. Three selected clips were decoded and checked. The complete archive remains remote.

The embedded YOLO `data.yaml` declares one class named `conveyor`, not foreign-object anomaly categories; its Roboflow metadata also states `license: Private`. The Mendeley record separately lists `yolo-v8-weights`, and the data paper describes these as weights used for center-region filtering. The annotated split contains 2,283 training, 96 validation, and 95 test images. Parsing the source-video IDs in image filenames found overlap across the supplied partitions: 17 shared IDs in train/test, 17 in train/validation, and 16 in validation/test. The file-level metadata does not independently alter or clarify the Mendeley record's displayed CC BY 4.0 license, but it shows that the supplied detector labels do not provide foreign-object targets and that the supplied split is not clip-held-out.

| Check | Observed evidence | Limit |
|---|---|---|
| Raw media | MP4 metadata reports 1280 × 720, 119.1829 FPS, 4,313 frames; all 4,313 frames decoded, giving 36.188 s at the reported rate. | OpenCV/container metadata was checked; no independent camera clock or timestamp sidecar was found. |
| Extracted-frame mapping | Five sampled JPEGs (IDs 2106, 2360, 2361, 2362, 2455) were compared with every decoded source frame at 160 × 90 grayscale. Each best match was the same numbered source-frame index; mean absolute pixel errors were 0.0122–0.0162 on a 0–255 scale. | This verifies the sampled ID mapping for the checked clip, not every dataset video. |
| Labels | The clip has 898 normal-labeled frames and 238 `annomaly`-labeled frames among 1,153 extracted images (98.53% folder-label coverage); 17 extracted images are unlabeled. Labeled runs: normal 2106–2360, anomaly 2362–2455, normal 2466–2685, anomaly 2688–2831, normal 2836–3258. | Folder membership supplies weak/manual frame labels. Annotation adjudication and inter-annotator reliability are not documented in the inspected materials. Do not fill the unlabeled gaps by interpolation. |
| Selected pilot | Frames 2250–2360 (111 normal) and 2362–2455 (94 anomaly) form a 205-image sequence. Frame 2361 is omitted because it is unlabeled. Source image IDs were matched to raw frame indices. | The one-frame omission compresses the sequence timeline after the gap by 8.39 ms. This is recorded and small relative to the 0.78 s labeled anomaly run. |
| Additional clip: wood_3 | 3,907/3,907 frames decoded at 117.8108 FPS; 1280 × 720. Five sampled IDs 2300, 2386, 2387, 2388, 2467 best matched same-index source frames (MAE 0.0131–0.0174). The selected sequence contains 87 normal IDs 2300–2386 and 80 anomaly IDs 2388–2467; unlabeled 2387 was omitted. | The derived sequence is 167 frames. Omitting one source frame compresses the timeline by about 8.49 ms. This does not verify independent clock accuracy or dataset-wide label reliability. |
| Additional clip: things | 4,982/4,982 frames decoded at 119.3415 FPS; 1280 × 720. Six sampled IDs 2840, 2881, 2888, 2958, 2962, 3017 best matched same-index source frames (MAE 0.0113–0.0166). The selected sequence has normal IDs 2840–2881, anomaly IDs 2888–2958, and normal IDs 2962–3017; nine unlabeled frames were omitted. | The derived sequence is 169 frames. Omitted gaps compress the timeline by about 75.4 ms. This remains a selected-clip check, not an independent camera clock. |
| Manual-split provenance spot check | Retrieved six small manual-split/source-image pairs for the three pilot clips. The normal pairs (IDs 2250, 2300, 2840) are byte-identical to the corresponding `image-files/<source-video>/` JPEGs (matching ZIP CRCs). The anomaly pairs (IDs 2362, 2388, 2888) have `_detected_1` renderings; the clip stem and counter match the same-index extracted source frames, and the displayed foreign-object regions are consistent. | This confirms representative file lineage and label-folder placement, not every label or its semantic correctness. `annomaly` is only a weak frame-level class label; no adjudication protocol or inter-rater reliability is available. |
| License | The Mendeley record displays CC BY 4.0. | Retain dataset attribution and DOI in every reuse. This record-level license statement does not independently verify rights for third-party material that may appear inside a frame. |

The accompanying [Data in Brief paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12175246/) describes a lab-scale conveyor with manually introduced foreign objects and extracted image subsets. It states that `image-files-manual-split` is derived from `image-files`, and that source-video names are retained with a sample counter at the front of each image name. The representative file check above supports that mapping for the three selected clips. The data remains a narrow conveyor/foreign-object dataset, not a broad industrial-process benchmark; annotations remain weak and partially labeled.

## Executed pilot and interpretation

The SAGE pilot uses three ordered, non-resized JPEG sequences and one manually labeled anomaly run per clip. It runs all four policies at budgets 0.10, 0.25, and 0.50, plus a five-condition simulated-cue ablation at 0.25. Exact outputs and aggregate tabled results are in [`PUBLIC_DATA_PILOT.md`](PUBLIC_DATA_PILOT.md). All four policies select the same exact quota within each clip and budget.

The cue simulator receives each event start as input. Sensor-triggered results are therefore oracle-derived, even though the video and labels come from a public dataset. They do not validate real sensors. Each selected clip contributes one weakly labeled positive run, and the baseline is MOG2 motion/activity rather than a foreign-object classifier. Treat three-event recall as descriptive; do not generalize it to other clips, cameras, or industrial settings. Report false-positive frame counts; do not treat adjacent positive frames as independent alarm episodes.

The pretrained OpenCV HOG model detects pedestrians, while this dataset labels conveyor foreign-object anomalies. Its output is not semantically comparable to the event labels. The embedded YOLO split labels the conveyor itself, not the foreign objects. An exploratory pretrained ResNet-18/ImageNet linear probe was added with heads trained on two clips and evaluated on a held-out third clip. The comparison is semantically aligned at the binary weak-label level, but annotation reliability, sample count, and dataset scope still limit it; results and methods are in [`PUBLIC_DATA_PILOT.md`](PUBLIC_DATA_PILOT.md). This does not validate a general anomaly detector.

## Provenance artifacts

- Raw subsets and extraction receipts: `data/raw/mendeley-conveyor/boardcamera_iron_ore_7_wood_2/`, `boardcamera_iron_ore_7_wood_3/`, and `boardcamera_iron_ore_things/`
- Derived pilot sequences, event intervals, and transformation records: `data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_2_labeled_transition_2250_2455/`, `boardcamera_iron_ore_7_wood_3_labeled_transition_2300_2467/`, and `boardcamera_iron_ore_things_labeled_transition_2840_3017/`
- Experiment results, event rows, and per-frame traces: `results/mendeley_conveyor_pilot_*`, `results/mendeley_conveyor_wood3_*`, and `results/mendeley_conveyor_things_*`
- Archive entry manifest produced from the ZIP central directory: `data/provenance/mendeley-conveyor/remote_zip_manifest.json` (local audit data, excluded from source control)
- Six-pair manual-split/source-image SHA-256 and ZIP CRC receipt: `docs/research/evidence/manual_split_provenance_check.json`

Raw and derived data remain ignored by version control. The project archive is not copied into `sources/`.

## Remaining validation work

1. Independently review annotation procedures and adjudicate selected event intervals; the three-clip timing/frame mapping check does not validate label truth.
2. Verify whether manual boxes or label files cover intervals rather than only selected frames; do not presume reliability from dense folder names.
3. Use independent sensor observations before making sensor-guidance claims.
4. Expand the ResNet linear-probe evaluation to more source-video groups with independently reviewed labels and held-out calibration; retain HOG only for worker-presence tasks.
5. Reserve IPAD for a later study after authors clarify dataset reuse rights and source timing.
6. Evaluate physical sensors and edge hardware next semester; current host runtime is not device latency, energy, or throughput evidence.

Scopus venue/source verification is documented separately in [`SCOPUS_SOURCE_AUDIT.md`](SCOPUS_SOURCE_AUDIT.md). It verifies Scopus source coverage for cited publication years using Elsevier's October 2026 source list; exact article-level DOI records were not individually verified.

## Sources

- [Mendeley dataset record](https://data.mendeley.com/datasets/s25x2bnshz/1), DOI 10.17632/s25x2bnshz.1.
- [Dataset description](https://pmc.ncbi.nlm.nih.gov/articles/PMC12175246/), *Data in Brief*, 2025, DOI 10.1016/j.dib.2025.111537.
- [IPAD official project page](https://ljf1113.github.io/IPAD_VAD/).
- [IPAD paper](https://arxiv.org/abs/2404.15033); peer-reviewed version DOI [10.1109/TCSVT.2024.3465517](https://doi.org/10.1109/TCSVT.2024.3465517).
- [IPAD Hugging Face mirror card](https://huggingface.co/datasets/MSherbinii/ipad-industrial-anomaly), treated as a secondary source rather than a dataset license grant.
