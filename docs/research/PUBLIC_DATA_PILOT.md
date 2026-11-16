# Public conveyor dataset pilot

**Run date:** 16 November 2026  
**Status:** executed and reproducible, descriptive three-clip pilot with weak/manual labels  
**Dataset:** de Sousa et al., *Image Dataset for Foreign Object Detection in Iron Ore Conveyor Belt Systems*, DOI 10.17632/s25x2bnshz.1. The [Mendeley record](https://data.mendeley.com/datasets/s25x2bnshz/1) displays CC BY 4.0.

## Data and evaluation setup

The 6.23 GB archive was inspected through HTTP range reads; the full archive was not downloaded. The selected ZIP members were selectively extracted with size and CRC verification. Three distinct source videos were decoded in full, and numbered JPEG samples were compared with decoded video frames at the same numeric source indices. Derived inputs contain ordered, original JPEGs, with unlabeled images omitted rather than interpolated.

| Source clip | Decoded source video | Pilot sequence | Label transition / event | Measured FPS | Timing note |
|---|---:|---:|---|---:|---|
| `boardcamera_iron_ore_7_wood_2` | 4,313 frames; 1280 × 720 | 205 frames, source IDs 2250–2455 | 111 normal (2250–2360), 94 anomaly (2362–2455); frame 2361 omitted | 119.1829 | Omission compresses derived timeline by about 8.39 ms after the gap. |
| `boardcamera_iron_ore_7_wood_3` | 3,907 frames; 1280 × 720 | 167 frames, source IDs 2300–2467 | 87 normal (2300–2386), 80 anomaly (2388–2467); frame 2387 omitted | 117.8108 | Omission compresses derived timeline by about 8.49 ms. |
| `boardcamera_iron_ore_things` | 4,982 frames; 1280 × 720 | 169 frames, source IDs 2840–3017 | 42 normal (2840–2881), 71 anomaly (2888–2958), 56 normal (2962–3017); 9 unlabeled frames omitted | 119.3415 | Gaps compress the derived timeline by about 75.4 ms in total. |

For each source, five or six sampled JPEGs were matched against decoded video at 160 × 90 grayscale. Each checked image's best match was its same-numbered source frame; mean absolute errors were 0.0113–0.0174 on a 0–255 scale. Six additional manual-split/source-image pairs were checked: the three normal files were byte-identical to their numbered source JPEGs, and three `_detected_1` anomaly renderings shared the matching clip stem and counter and showed the corresponding object regions. This supports representative file lineage and sampled-ID mapping, not independent camera-clock accuracy, dataset-wide timing, or the truth of every label. Labels come from manually organized folders, including the source spelling `annomaly`; annotation adjudication and inter-annotator reliability are not established. Each selected anomalous run is treated as one event solely for this pilot.

The cue simulator is seeded from the same event annotation used by the evaluator. Every sensor-assisted row is therefore oracle-derived. This does not measure independent sensors. MOG2 measures visual activity/change, not foreign-object identity. The video and runs describe a lab-scale conveyor dataset, not a broad industrial benchmark.

## Matched-budget MOG2 results

All four policies received each clip and seed 17, and selected the same quota within a clip/budget. Aggregate rows below sum detections and false-positive analyzed frames across the three clips; event recall is shown as detected/three events. Because each clip contributes only one weakly labeled interval and there is one run per condition, these are descriptive counts rather than a statistical policy ranking. False-positive frames are detector-positive analyzed frames outside labeled intervals; consecutive frames are not merged into alarm episodes. Host runtime includes the scout pass for video-adaptive and budget-aware policies, but excludes decoding, scheduling overhead, and file writing.

| Budget | Policy | Event recall across clips | Total analyzed frames | False-positive frames |
|---:|---|---:|---:|---:|
| 0.10 | Fixed-rate | 3/3 | 55 | 28 |
| 0.10 | Video-adaptive | 0/3 | 55 | 46 |
| 0.10 | Sensor-triggered* | 3/3 | 55 | 24 |
| 0.10 | Budget-aware* | 0/3 | 55 | 46 |
| 0.25 | Fixed-rate | 3/3 | 137 | 73 |
| 0.25 | Video-adaptive | 0/3 | 137 | 128 |
| 0.25 | Sensor-triggered* | 3/3 | 137 | 59 |
| 0.25 | Budget-aware* | 0/3 | 137 | 128 |
| 0.50 | Fixed-rate | 3/3 | 272 | 144 |
| 0.50 | Video-adaptive | 1/3 | 272 | 221 |
| 0.50 | Sensor-triggered* | 3/3 | 272 | 116 |
| 0.50 | Budget-aware* | 1/3 | 272 | 221 |

`*` Cue-assisted policies receive event-start cues generated from the same annotation used by the evaluator. These are oracle-derived results, not independent sensor results. At 25%, per-clip false-positive frames (wood_2 / wood_3 / things) were fixed-rate 28/21/24, video-adaptive 49/39/40, sensor-triggered 27/22/10, and budget-aware 49/39/40.

Per-clip event outcomes behind the aggregate are:

| Clip | Fixed-rate, all budgets | Video-adaptive, 10% / 25% / 50% | Sensor-triggered*, all budgets | Budget-aware*, 10% / 25% / 50% |
|---|---:|---:|---:|---:|
| wood_2 transition | 1/1 | 0/1 / 0/1 / 0/1 | 1/1 | 0/1 / 0/1 / 0/1 |
| wood_3 transition | 1/1 | 0/1 / 0/1 / 0/1 | 1/1 | 0/1 / 0/1 / 0/1 |
| things transition | 1/1 | 0/1 / 0/1 / 1/1 | 1/1 | 0/1 / 0/1 / 1/1 |

In these runs, fixed-rate detected all three labeled events at each budget. MOG2-driven video-adaptive and budget-aware scheduling detected none at 10% and 25%, and one of three at 50%. The selected clip set therefore shows that activity-based selection can miss labeled events at these quotas; it does not show that fixed-rate will generalize better. Sensor-triggered recall was 3/3, but that result is not independent evidence: cues use the labeled event starts, and deterministic fallback can also detect events. Higher quota generally raises the number of positive analyzed frames; the counts are not normalized alarm-episode metrics. No edge savings or energy is measured.

## Cue ablation at 25%

Five cue conditions were run for four policies on each of three clips (60 rows total). The ablation is retained in the per-clip result folders `results/mendeley_conveyor_pilot_ablation/`, `results/mendeley_conveyor_wood3_ablation/`, and `results/mendeley_conveyor_things_ablation/`. It is a controlled simulator sensitivity check: cue seeds begin with the labeled event start, so it does not estimate real sensor performance. The sensor-triggered no-cue condition is a necessary baseline because deterministic fallback sampling may cover events without cues. Refer to each `results.csv`, event rows, and frame traces instead of pooling these repeated policy decisions as independent samples.

## Pretrained-model semantic check

The OpenCV HOG plus linear-SVM pedestrian detector was run at 25% on the first clip for all four policies. It produced zero event recall and zero false-positive frames. This is **not** a valid anomaly-model comparison: the weights detect pedestrians, while the labels describe conveyor foreign objects. It is retained only as a semantic-mismatch diagnostic.

The dataset archive includes YOLO image splits (2,283 train, 96 validation, and 95 test images). The Mendeley record separately lists `yolo-v8-weights`; the data paper says these weights were used to filter the belt's center region. The checked `data.yaml` defines a single class, `conveyor`, rather than foreign-object anomaly classes; its embedded Roboflow metadata says `license: Private`. The source-video identifiers overlap heavily across the supplied splits (17 shared between train and test, 17 between train and validation, and 16 between validation and test), so those splits are unsuitable for an unbiased clip-held-out detector result. The embedded Roboflow metadata does not override or independently clarify the Mendeley archive's displayed CC BY 4.0 terms.

### Clip-held-out pretrained ResNet probe

To add a semantically aligned image-level ML comparator without using the mismatched conveyor-box labels, an Apache-2.0 ONNX Model Zoo ResNet-18 v1-7 pretrained on ImageNet was used as a frozen feature extractor. Its 1,000 ImageNet logits feed a class-balanced logistic linear head trained on weak/manual normal/anomaly folder labels from the other two selected clips. Each clip is evaluated only by its corresponding held-out head (three-fold leave-one-source-video-out). No held-out labels were used for fitting or threshold selection; the classification threshold is 0.5. The fold heads were trained on 336, 374, and 372 labeled images, respectively. This is exploratory transfer learning over three selected clips, not an industrially validated anomaly detector or full-network fine-tuning.

The SAGE engine ran all four sampling policies at the same exact per-clip quotas used by MOG2. The cue-assisted rows remain oracle-derived. Numbers below sum the three held-out clips. Runtime is the sum of timed detector processing across clips/policies, with model/session initialization and media decoding excluded.

| Budget | Policy | Event recall | False-positive frames | Total selected frames | Host detector runtime (s) |
|---:|---|---:|---:|---:|---:|
| 0.10 | Fixed-rate | 3/3 | 13 | 55 | 1.220 |
| 0.10 | Video-adaptive | 0/3 | 13 | 55 | 3.735 |
| 0.10 | Sensor-triggered* | 3/3 | 7 | 55 | 1.198 |
| 0.10 | Budget-aware* | 0/3 | 13 | 55 | 3.755 |
| 0.25 | Fixed-rate | 3/3 | 25 | 137 | 2.891 |
| 0.25 | Video-adaptive | 0/3 | 38 | 137 | 5.393 |
| 0.25 | Sensor-triggered* | 3/3 | 22 | 137 | 2.822 |
| 0.25 | Budget-aware* | 0/3 | 38 | 137 | 5.347 |
| 0.50 | Fixed-rate | 3/3 | 51 | 272 | 5.681 |
| 0.50 | Video-adaptive | 1/3 | 75 | 272 | 8.129 |
| 0.50 | Sensor-triggered* | 3/3 | 45 | 272 | 5.529 |
| 0.50 | Budget-aware* | 1/3 | 75 | 272 | 7.937 |

At 25%, the ResNet probe and MOG2 produced the same event-recall pattern across policies (3/3 fixed, 0/3 video-adaptive, 3/3 cue-assisted sensor, 0/3 budget-aware), while the ResNet probe produced fewer false-positive frames (25/38/22/38 versus 73/128/59/128). Its measured host processing time was higher (for fixed-rate, 2.891 s summed across clips versus 0.736 s for MOG2). This is a small weak-label comparison; it suggests a workload/false-positive trade-off worth testing, not a general accuracy or efficiency claim. All runs are one seed with three events, no external clip set, and no independent labels.

The ONNX base model and license/source record are documented in `models/pretrained/README.md`. The training workflow is `scripts/train_resnet18_probe.py`; fold heads and summary are under `models/linear-probes/`. To reproduce head fitting, run `python -m scripts.train_resnet18_probe`. Each SAGE output folder is `results/mendeley_resnet18_probe_cv_<clip>_budget_<010|025|050>/`; the result rows retain model/head paths, exact quotas, timings, event outcomes, and frame traces.

## Reproduction and result files

For each clip, the CLI uses the clip-specific derived folder, its `events.csv`, measured FPS, budget, seed 17, and a distinct output directory. Budgets 0.10, 0.25, and 0.50 are run for each of the three clips; `--ablation` at 0.25 generates the cue-condition rows. Each run folder contains policy CSV/JSONL, event CSV/JSONL, and per-frame trace CSV/JSONL. Provenance JSON records source IDs, frame mappings, measured FPS, label derivation, omitted gaps, and local file hashes. The source ZIP hash is taken from Mendeley metadata, not from a locally downloaded full archive.

- Clip 1: `data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_2_labeled_transition_2250_2455/`; outputs `results/mendeley_conveyor_pilot_budget_{010,025,050}/` and `_ablation/`.
- Clip 2: `data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_3_labeled_transition_2300_2467/`; outputs `results/mendeley_conveyor_wood3_budget_{010,025,050}/` and `_ablation/`.
- Clip 3: `data/derived/mendeley-conveyor/boardcamera_iron_ore_things_labeled_transition_2840_3017/`; outputs `results/mendeley_conveyor_things_budget_{010,025,050}/` and `_ablation/`.
- The HOG negative control is in `results/mendeley_conveyor_pilot_hog_semantic_negative_control/`.

Raw/derived media are ignored user data. The synchronized `sources/` directory has not been modified.

## Conclusions supported by this run

The workflow now ingests three selected public conveyor clips with checked source-frame mapping, retains exact matched quotas, and emits per-policy traces and metrics. Across these three selected weak-label events, fixed-rate detected 3/3 at all tested budgets; MOG2-driven video-adaptive scheduling detected 0/3 at 10% and 25%, and 1/3 at 50%. This descriptive pattern is not a general policy ranking. Oracle-derived cue results do not establish sensor benefit; MOG2 and HOG do not constitute a semantically valid anomaly-model comparison; labels are not independently validated; and there are no held-out clips, repeated seeds, physical sensors, edge measurements, or energy measurements. The pilot narrows but does not close the validation gap.
