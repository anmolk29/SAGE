# SAGE Usage Guide

Commands below match the current `python -m sage` CLI. Run them from the project root (the folder containing `requirements.txt`, `sage/`, and `app.py`). The three Mendeley conveyor clips used in the pilot are local, Git-ignored data; they are not bundled in a fresh repository checkout. See [Dataset and provenance](DATASET_AND_PROVENANCE.md) and [Dataset validation](research/DATASET_VALIDATION.md) for setup context and evidence. IPAD was not used in the reported pilot.

## 1. Create the Python environment

In PowerShell, from the project root:

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The code declares Python 3.10 or newer. If Python 3.11 is unavailable, use an installed supported version with `py -3 -m venv .venv`. Dependencies include OpenCV and NumPy for processing, plus Streamlit, pandas, and matplotlib for the dashboard.

## 2. Run the synthetic end-to-end demo

```powershell
python -m sage demo --output results/demo
```

This creates a small synthetic sequence locally and runs the four scheduling policies without external video or dataset downloads. The demo is a pipeline smoke run, not evidence about real industrial data or physical sensors. It writes:

- `results/demo/results.csv` and `results/demo/results.jsonl` — policy-level experiment records.
- `results/demo/event_results.csv` and `results/demo/event_results.jsonl` — event-level type, hit/miss, and latency records.
- `results/demo/frame_trace.csv` and `results/demo/frame_trace.jsonl` — scheduling/detection trace.
- `results/demo/events.csv` — synthetic demonstration annotations.
- `results/demo/synthetic_frames/` — generated demo images.

## 3. Prepare event annotations

Create a UTF-8 CSV file with a header containing `start_s,end_s` and an optional `label` column. Times are seconds on the clip's timeline; each row is one event interval. Use non-negative numeric values and ensure `end_s >= start_s`. Intervals are inclusive for evaluator matching. Labels are descriptive and do not affect scheduling or detector decisions.

```csv
start_s,end_s,label
1.20,3.20,conveyor_object_motion
4.80,5.90,sorting_event
```

Save it, for example, as `data/annotations/clip01.csv`. Confirm that these intervals use the same timeline as the input video. For a frame sequence without original timestamps, choose and record an explicit replay rate; convert annotated frame indices to seconds using that declared rate. If the source timing cannot be verified, interpret latency only as frame/replay-time latency and disclose the assumption. Do not use anomaly labels as sensor cues; the simulator generates cues from event intervals while the scheduler only receives the generated cue stream.

## 4. Run a real clip or ordered image sequence

The CLI accepts either a video file or a directory containing a single sequence of image frames. For a folder, only image files directly inside that directory are read, sorted by natural filename order. Pass the sequence's documented frame rate with `--fps`; absent an override, the current loader assumes 1 FPS for an image directory. Do not use a guessed FPS as source timing.

Example with a video file:

```powershell
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/clip01.csv" --output "results/clip01" --seed 17 --detector motion
```

Example with an ordered frame directory and a verified/declared replay rate of 10 frames per second:

```powershell
python -m sage --video "data/raw/clip01_frames" --events "data/annotations/clip01.csv" --output "results/clip01_frames" --seed 17 --fps 10 --detector motion
```

The command runs all four policies by default: fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware. Every policy receives the same exact frame quota, `ceil(total_frames × budget_fraction)`, so their comparisons are paired at equal analyzed-frame counts. `--budget FRACTION` sets that common quota; repeat the command with low, medium, and high values to produce a budget curve. Other optional arguments include `--cue-probability P`, `--false-triggers-per-minute RATE`, `--cue-delay SECONDS`, `--clip-id ID`, `--data-source LABEL`, and `--policies POLICY [POLICY ...]`. The default seed is 7; set it explicitly when recording a run.

Example matched-budget runs:

```powershell
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/clip01.csv" --output "results/clip01_budget10" --seed 17 --budget 0.10
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/clip01.csv" --output "results/clip01_budget25" --seed 17 --budget 0.25
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/clip01.csv" --output "results/clip01_budget50" --seed 17 --budget 0.50
```

## 5. Run cue-quality ablations

Add `--ablation` to run the cue-quality matrix on the same clip:

```powershell
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/clip01.csv" --output "results/clip01_ablation" --seed 17 --detector motion --ablation
```

The cue detection probability, false-trigger rate, delay, and random seed describe a **simulator**, not physical sensor measurements. Record the clip and source timing validation alongside exported results.

## 6. Compare detectors responsibly

The choices are `motion`, `hog_people`, and `resnet18_probe`:

- `motion` is a classical OpenCV foreground/motion detector. It flags visual activity and does not identify semantic anomalies.
- `hog_people` uses OpenCV's built-in pretrained HOG plus linear-SVM pedestrian detector. It detects people/workers and is not a general industrial anomaly detector.
- `resnet18_probe` uses ImageNet-pretrained ResNet-18 logits and a binary logistic head fit on weak/manual labels. For the public pilot, each head trains on two source clips and is evaluated on the held-out third.

To compare them, run the same clip, event intervals, policies, seed, timing, and other settings twice, changing only `--detector`. Compare results only where event labels match the detector's semantics. For example, worker-presence events can be appropriate for `hog_people`; conveyor motion, sorting errors, or general anomaly labels are not equivalent targets. Do not present scores across different event definitions as a direct model comparison.

Example:

```powershell
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/workers.csv" --output "results/clip01_motion" --seed 17 --detector motion
python -m sage --video "data/raw/clip01.mp4" --events "data/annotations/workers.csv" --output "results/clip01_hog" --seed 17 --detector hog_people
```

For the bundled three-clip pilot, regenerate held-out heads with `python -m scripts.train_resnet18_probe`, then run the matching head using the same clip, event file, seed, FPS, budget, and policies as the baseline. Example for wood_2 held out:

```powershell
python -m sage --video "data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_2_labeled_transition_2250_2455" --events "data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_2_labeled_transition_2250_2455/events.csv" --output "results/resnet18_wood2_25" --fps 119.18288018385427 --seed 17 --budget 0.25 --detector resnet18_probe --model-path "models/pretrained/resnet18-v1-7.onnx" --head-path "models/linear-probes/resnet18_probe_heldout_wood2.json"
```

The head uses weak/manual labels from the other two clips and a fixed 0.5 probability threshold. This is an exploratory transfer-learning baseline, not full ResNet fine-tuning or a validated industrial anomaly model. See `docs/research/PUBLIC_DATA_PILOT.md` for all three folds and results.

## 7. Output files and interpretation

Each run output directory contains `results.csv` and `results.jsonl`, `event_results.csv` and `event_results.jsonl`, and (when generated) `frame_trace.csv` and `frame_trace.jsonl`. The CLI prints the paths it wrote. Summary rows contain clip, detector, policy, seed and cue settings, aggregate event metrics, frame counts, timing/runtime, and run metadata. Event-level rows retain each event type, hit/miss, and latency. Trace rows retain per-frame scheduling and detection decisions.

`results.csv` is suitable for the Streamlit dashboard. Start it from the project root with:

```powershell
streamlit run app.py
```

Select the relevant result CSV in the dashboard. Aggregate dashboard values describe the loaded software runs. Runtime is measured on the current host; budget and cue parameters are experimental/simulated. Neither represents Raspberry Pi performance, physical sensor behavior, or energy consumption.

## 8. Keep media and generated outputs organized

- Store downloaded raw media under `data/raw/` and annotations under `data/annotations/`; the repository ignore rules exclude `data/**` except `data/.gitkeep`.
- Keep derived/conversion files separate from raw source and document resizing, frame extraction, timing assumptions, and exclusions.
- Store experiment outputs under `results/<run-name>/`; `results/**` is excluded from version control except `results/.gitkeep`.
- Do not put large archives, raw frames, private recordings, or training checkpoints in Git. The repository includes only the Apache-2.0 ResNet-18 weights required for the documented probe; provenance and checksum are recorded in `models/pretrained/README.md`.

For current dataset access and validation steps, see [DATASET_AND_PROVENANCE.md](DATASET_AND_PROVENANCE.md). For the project requirements and implemented/simulated/planned boundaries, see [SAGE_SPECIFICATION.md](SAGE_SPECIFICATION.md).
