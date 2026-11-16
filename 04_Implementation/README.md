# SAGE

**Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring**

SAGE is a software research prototype for comparing video sampling policies on industrial monitoring clips. Its research question is whether simulated low-cost sensor cues improve event coverage and latency under a fixed analysis budget, compared with fixed-rate and video-only sampling.

## Status and scope

| Component | Status |
| --- | --- |
| Industrial video input and public-data workflow | Software supports video/image sequences; IPAD is the selected public dataset candidate. Its full archive has not been downloaded or validated in this workspace. |
| Classical CV | OpenCV motion-based baseline. |
| Pretrained ML | OpenCV's pretrained HOG person detector is the low-dependency comparator when enabled. It detects people only; it is not a general industrial anomaly detector. |
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

Open the dashboard:

```powershell
streamlit run app.py
```

The exact CLI options and annotation format are documented in `docs/USAGE.md`. A run records its configuration, software timing, detector, seed, and per-frame decisions. Keep source data outside version control; see `.gitignore`.

## Evaluation rules

- Compare policies on the same clip, annotations, detector, and sensor-cue realization.
- Ground-truth annotations are evaluation-only; the scheduler and detector must not read them.
- Freeze detector settings before held-out evaluation.
- Report event recall, false alarms per clip-minute, detection latency (with misses), analyzed-frame fraction, and host software runtime.
- Treat dataset-specific findings as bounded to the clips and event definitions actually evaluated.
- Do not interpret simulated budgets as edge-device capacity, software time as energy, or simulated cues as physical sensors.

## Repository map

- `sage/`: experiment engine and policy implementations.
- `app.py`: Streamlit result explorer.
- `tests/`: deterministic component and end-to-end checks.
- `docs/`: specification, usage, dataset/provenance, manuscript, and future hardware plan.
- `results/`: generated summary, per-event, and per-frame trace outputs (ignored by Git).
- `data/`: user-downloaded clips and annotations (ignored by Git).

## Research status

The manuscript is a submission-style draft and protocol, not a report of fabricated experimental results. It marks empirical sections for completion from actual runs. Read `docs/` before using results or making claims.
