# SAGE

**Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring**

SAGE is a software research prototype for comparing video sampling policies on industrial monitoring clips. Its research question is whether simulated low-cost sensor cues improve event coverage and latency under a fixed analysis budget, compared with fixed-rate and video-only sampling.

## Status and scope

| Component | Status |
| --- | --- |
| Industrial video input and public-data workflow | Three selected weak-label Mendeley conveyor clips have been evaluated. IPAD remains out of scope until dataset rights, timing, and annotation reliability are clarified. |
| Classical CV | OpenCV motion-based baseline. |
| Pretrained ML | Exploratory ImageNet-pretrained ResNet-18 with a clip-held-out logistic head is compared against MOG2 on three weak-label clips; HOG remains a pedestrian-only diagnostic. |
| Sensor inputs | Simulated timestamped cues with configurable misses, false triggers, delay, and seed. No physical sensor data is used. |
| Scheduling | Fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware adaptive policies. |
| Benchmarks | Reproducible per-run traces and metrics; software time is measured on the host, while budgets are modeled. |
| Dashboard | Streamlit UI reads experiment results. |
| Hardware | Future work only: camera, sensor/microcontroller, and edge computer integration. No Raspberry Pi or energy results are claimed. |

The four supplied project documents remain unchanged as reference material. The implementation and new deliverables live alongside them.

## Quick start

Use Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m sage --help
```

Run the synthetic reproducibility demo (requires no downloaded video):

```powershell
python -m sage demo --output results/demo
```

Run on a video clip with event annotations:

```powershell
python -m sage --video data/clip.mp4 --events data/annotations.csv --output results/run --seed 17
```

To regenerate the three source-video-held-out ResNet-18 linear heads, run `python -m scripts.train_resnet18_probe`. Its outputs use the included Apache-2.0 ONNX Model Zoo weights and the weak/manual labels recorded in the selected clip provenance files.

Open the dashboard:

```powershell
streamlit run app.py
```

Run the automated checks:

```powershell
python -m unittest discover -s tests -v
```

The exact CLI options and annotation format are documented in `docs/USAGE.md`. A run records its configuration, software timing, detector, seed, and per-frame decisions. Keep source data outside version control; see `.gitignore`.

## Evaluation rules

- Compare policies on the same clip, annotations, detector, and sensor-cue realization.
- Ground-truth annotations go to the evaluator. In the current controlled simulator, event starts also seed simulated cues; sensor-guided runs are therefore oracle-derived, not independent sensor evidence.
- Freeze detector settings before held-out evaluation.
- Report event recall, false alarms per clip-minute, detection latency (with misses), analyzed-frame fraction, and host software runtime.
- Treat dataset-specific findings as bounded to the clips and event definitions actually evaluated.
- Do not interpret simulated budgets as edge-device capacity, software time as energy, or simulated cues as physical sensors.

## Repository map

- `sage/`: experiment engine and policy implementations.
- `app.py`: Streamlit result explorer.
- `tests/`: deterministic component and end-to-end checks.
- `docs/`: specification, usage, dataset/provenance, manuscript, and future hardware plan.
- `paper/overleaf/`: Overleaf upload package with IEEE conference LaTeX source and BibTeX references.
- `docs/research/LITERATURE_MATRIX.md`: 20-source focused research map with relevance and Scopus-verification caveat.
- `docs/research/SCOPUS_SOURCE_AUDIT.md`: official October 2026 venue/year coverage check; exact article records remain unverified.
- `docs/research/DATASET_VALIDATION.md`: verified subset evidence, rights/timing/annotation gates, and limitations.
- `docs/research/RESEARCH_GAP_AND_METHOD.md`: defensible project question and fair evaluation protocol.
- `docs/research/SYNTHETIC_RUN_RECORD.md`: fresh matched-budget synthetic sweep and its limits.
- `docs/research/PUBLIC_DATA_PILOT.md`: three-clip MOG2 and ResNet-probe results, annotation-derived cue caveat, and detector limitations.
- `docs/research/evidence/manual_split_provenance_check.json`: checksums and source-file mapping for six representative dataset frames.
- `scripts/dataset_audit/`: range-based public archive inspection and selective extraction helpers.
- `data/provenance/mendeley-conveyor/`: local archive manifest and three retained anomaly-image samples used in the provenance check; raw data and provenance files are excluded from source control.
- `scripts/train_resnet18_probe.py`: reproducible three-fold, source-video-held-out linear-head training.
- `models/pretrained/README.md`: ResNet-18 model source, license, preprocessing, and checksum.
- `models/linear-probes/`: generated heads, each trained on two clips and reserved for its held-out third clip.
- `docs/academic/PRESENTATION_AND_VIVA_GUIDE.md`: system explanation, slide outline, four-hour study plan, and viva questions.
- `presentation-output/SAGE_Research_Presentation_v11.pptx`: current editable 12-slide project presentation with full references and the ResNet-probe comparison. Superseded iterations are archived and marked superseded.
- `results/`: generated summary, per-event, and per-frame trace outputs (ignored by Git).
- `data/`: user-downloaded clips and annotations (ignored by Git).

The final study runs and their scope limits are documented in `docs/research/`. The files in `results/` are retained as experiment evidence; temporary demo and smoke-test outputs were removed. The four supplied Word documents at the project root remain unchanged reference material.

## Research status

The manuscript now contains a bounded three-clip public-data pilot with a clip-held-out ResNet-18 linear probe. Sensor cues derive from labels, event labels are weak/manual, and the results are exploratory. HOG does not match foreign-object label semantics. Elsevier's October 2026 source list covers all cited venues for their publication years; exact article-level Scopus records remain unverified. Read the research records before using results or making claims.
