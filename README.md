# SAGE

**Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring**

SAGE is a reproducible software study of four video-frame scheduling policies under matched analysis budgets. It includes classical computer vision, an exploratory clip-held-out ResNet-18 probe, a controlled sensor-cue simulator, saved experiment traces, and a Streamlit results explorer.

## Current status

The public-data pilot covers three selected weak-label conveyor clips. The event labels are weak/manual, and simulated cues derive from event starts, so sensor-guided results are oracle-derived. The results are descriptive and do not establish general anomaly-detection accuracy, physical sensor benefit, edge-device performance, or energy savings. Physical sensor and hardware work is documented as future work.

## Run the project

Use Python 3.10 or newer. From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m sage --help
```

Run the synthetic demo without downloading video:

```powershell
python -m sage demo --output results/demo
```

Run the dashboard:

```powershell
streamlit run app.py
```

Run the automated checks:

```powershell
python -m unittest discover -s tests -v
```

For video inputs, event annotation format, and dataset provenance, see [Usage](docs/USAGE.md) and [Dataset and provenance](docs/DATASET_AND_PROVENANCE.md).

## Research and presentation files

- [IEEE-style manuscript draft](docs/IEEE_MANUSCRIPT_DRAFT.md)
- [Research literature matrix](docs/research/LITERATURE_MATRIX.md)
- [Research gap and evaluation method](docs/research/RESEARCH_GAP_AND_METHOD.md)
- [Dataset validation record](docs/research/DATASET_VALIDATION.md)
- [Scopus source-year audit](docs/research/SCOPUS_SOURCE_AUDIT.md); individual DOI records were not verified in Scopus
- [Three-clip public-data pilot](docs/research/PUBLIC_DATA_PILOT.md)
- [Four-hour study and viva guide](docs/academic/PRESENTATION_AND_VIVA_GUIDE.md)
- [Overleaf package and instructions](paper/overleaf/README.md)
- [Current 12-slide presentation](presentation-output/SAGE_Research_Presentation_v11.pptx)
- [Original project reference documents](docs/reference-material/)

## Repository layout

- `sage/` — experiment engine, scheduling policies, CLI, and detector support.
- `app.py` — Streamlit results dashboard.
- `tests/` — deterministic checks for the engine, policies, and model probe.
- `scripts/` — dataset inspection and held-out model training utilities.
- `docs/` — usage, protocol, research evidence, manuscript, and hardware extension plan.
- `models/` — pretrained ResNet-18 weights and clip-held-out probe records.
- `paper/overleaf/` — IEEEtran source, BibTeX references, and upload-ready ZIP.
- `presentation-output/` — current presentation.
- `archive/` — older numbered repository folders consolidated for history; not the active source tree.

Raw video data, derived clip data, and per-run result folders stay local and are excluded from Git. The included ResNet-18 weights are Apache-2.0; details and checksum are in `models/pretrained/README.md`.
