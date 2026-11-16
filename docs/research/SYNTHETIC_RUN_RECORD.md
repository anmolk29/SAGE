# Synthetic run record

**Run date:** 15 November 2026  
**Input:** SAGE-generated 70-frame toy sequence, 10 FPS, two synthetic event intervals  
**Data source:** `synthetic_demo`  
**Detector:** OpenCV MOG2  
**Policy seed:** 17  
**Public dataset:** none  
**Interpretation:** pipeline/reproducibility check only; not industrial performance evidence.

## Matched-budget sweep

| Target fraction | Exact quota | Policy | Events hit | Events total | Recall | Misses | Frame false positives | Mean latency (s) |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 0.10 | 7 | fixed_rate | 1 | 2 | 0.50 | 1 | 0 | 0.8 |
| 0.10 | 7 | video_adaptive | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.10 | 7 | sensor_triggered | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.10 | 7 | budget_aware | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.25 | 18 | fixed_rate | 1 | 2 | 0.50 | 1 | 0 | 0.3 |
| 0.25 | 18 | video_adaptive | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.25 | 18 | sensor_triggered | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.25 | 18 | budget_aware | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.50 | 35 | fixed_rate | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.50 | 35 | video_adaptive | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.50 | 35 | sensor_triggered | 1 | 2 | 0.50 | 1 | 0 | 0.0 |
| 0.50 | 35 | budget_aware | 1 | 2 | 0.50 | 1 | 0 | 0.0 |

The 12 rows are saved as CSV, JSONL, event rows, and frame traces in `results/verified_sweep_0.10/`, `results/verified_sweep_0.25/`, and `results/verified_sweep_0.50/`. A separate fresh default demo (`results/verified_synthetic_20261115/`) and 20-row five-condition cue ablation (`results/verified_synthetic_20261115_ablation/`) were also executed.

The fixture is intentionally tiny and synthetic, the cue simulator is derived from event annotations, only two events are present, and the detector reports motion rather than industrial anomaly semantics. The equal 0.50 recall across this fixture does not establish that policies are equivalent or that sensor guidance helps. Host runtime from these short runs is not suitable for performance comparison or resource claims.

## Reproduction

```powershell
python -m unittest discover -s tests -v
python -m sage demo --output results/verified_synthetic_20261115
python -m sage --video results/verified_synthetic_20261115/synthetic_frames --events results/verified_synthetic_20261115/events.csv --output results/verified_sweep_0.10 --fps 10 --seed 17 --budget 0.10
python -m sage --video results/verified_synthetic_20261115/synthetic_frames --events results/verified_synthetic_20261115/events.csv --output results/verified_sweep_0.25 --fps 10 --seed 17 --budget 0.25
python -m sage --video results/verified_synthetic_20261115/synthetic_frames --events results/verified_synthetic_20261115/events.csv --output results/verified_sweep_0.50 --fps 10 --seed 17 --budget 0.50
python -m sage --video results/verified_synthetic_20261115/synthetic_frames --events results/verified_synthetic_20261115/events.csv --output results/verified_synthetic_20261115_ablation --fps 10 --seed 17 --budget 0.25 --ablation
```
