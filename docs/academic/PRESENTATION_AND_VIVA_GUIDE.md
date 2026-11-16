# SAGE presentation and four-hour preparation guide

## One-minute project explanation

SAGE stands for Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring. It asks whether a monitoring system can analyze fewer video frames while preserving event coverage. It compares fixed-rate, motion-adaptive, simulated sensor-triggered, and combined budget-aware sampling at the same frame budget. I ran a bounded pilot on three selected weakly labeled iron-ore conveyor clips. Fixed-rate detected 3/3 labeled intervals at all three budgets with both MOG2 and an exploratory pretrained ResNet-18 linear probe. At 25%, the probe produced fewer false-positive frames than MOG2, with higher host processing time. Each linear head trained on two clips and was tested on the held-out third. Sensor-triggered recall was 3/3, but cues came from annotations, so the result is oracle-assisted. These three weak-label events do not establish general industrial performance. Hardware and edge-energy claims remain next-semester work.

## End-to-end system, in order

1. **Input:** a video or ordered image sequence, plus separate event intervals for evaluation.
2. **Scout:** for video-adaptive policies, MOG2 computes a lightweight frame activity score. This is a visual-change signal, not semantic anomaly understanding.
3. **Cue simulator:** generates seeded cues from annotated event starts with declared miss probability, false-trigger rate, and delay. Because event labels drive this simulator, cues are oracle-derived controlled inputs rather than independent sensor measurements.
4. **Scheduler:** one of four policies chooses exactly `ceil(frame_count × budget_fraction)` frames. Fixed-rate spreads selections uniformly. Video-adaptive favors motion scores. Sensor-triggered favors active cue windows. Budget-aware favors either current motion or a cue, then fills quota deterministically.
5. **Detector:** selected frames go to MOG2, HOG+SVM, or the ResNet-18 linear probe. MOG2 reports foreground change; HOG reports pedestrian presence only; the ResNet probe scores binary normal/anomaly appearance using a head trained on other source clips.
6. **Evaluator:** separate event annotations are matched to positive detections to count detected/missed events, frame-level false positives, and latency. Labels must never inform the scheduler except through the explicitly identified cue simulator.
7. **Artifacts/dashboard:** the CLI writes summary rows, event rows, and frame traces; the Streamlit app filters saved runs and compares results.

## Current evidence to present accurately

- The unittest suite passed **10/10 tests** after adding the ResNet linear-probe implementation.
- A fresh synthetic demo produced 4 policy rows over 70 generated frames at 10 FPS; each policy analyzed 18 frames (25% target rounds up to 18). Each policy detected 1 of 2 generated events (0.5 recall), missed 1, and had one frame-level false alarm. These values describe the synthetic fixture only.
- A fresh five-condition ablation generated 20 rows (four policies × five cue conditions). The tiny synthetic fixture produced 0.5 recall for every row; it does not establish cue effects.
- Selective range downloads retrieved three source MP4s and sampled JPEGs from Mendeley Data; ZIP CRC and size checks passed. A six-file spot check found byte-identical normal source/manual-split JPEGs and matching clip stems/counters for three anomaly renderings. This confirms sample lineage, not annotation truth. The record displays CC BY 4.0.
- The clips report 119.1829, 117.8108, and 119.3415 FPS, with 4,313, 3,907, and 4,982 decoded frames at 1280 × 720. Five or six sampled image IDs per clip matched same-index decoded source frames.
- The derived pilot sequences contain 205, 167, and 169 frames with one weakly labeled event each. At 10%, 25%, and 50%, fixed-rate recall was 3/3 at every budget; video-adaptive and budget-aware recall was 0/3, 0/3, and 1/3; sensor-triggered recall was 3/3 at each budget. Sensor cues derive from event labels.
- At 25% budget across three clips, MOG2 returned 73/137 false-positive frames for fixed-rate, 128/137 for video-adaptive, 59/137 for sensor-triggered, and 128/137 for budget-aware. These are analyzed-frame counts, not merged alarms. MOG2 measures activity, not object identity.
- The ResNet-18/ImageNet linear probe was evaluated with a three-fold source-video-held-out design. At 25%, it matched MOG2 event recall and returned 25/137, 38/137, 22/137, and 38/137 false-positive frames (fixed/video/sensor/budget). Its summed fixed-rate host detector runtime was 2.891 seconds versus 0.736 for MOG2. The head was fit on weak/manual labels from the other two clips, and the probability threshold was fixed at 0.5.
- The HOG pedestrian detector was run for all four policies at 25%, with 0/1 event recall and 0 false-positive frames. Because labels describe foreign-object anomalies, these values are a semantic-mismatch diagnostic, not a direct detector comparison.
- IPAD remains a good topical fit and a peer-reviewed IEEE TCSVT paper, but its video reuse terms, original timing, and annotation reliability remain unverified. The project website license is not a dataset license.

## Suggested 9 content slides plus references

1. **Problem:** every-frame analytics can waste compute during quiet periods; goal is to study a recall/latency/workload trade-off.
2. **Research question:** four policies, same video and exact frame budget; do simulated cues help, and when do cue errors hurt?
3. **Research foundation:** edge video analytics; adaptive configuration/scheduling; sensor-aware edge video analytics; industrial video anomaly datasets. Cite the literature matrix, not the GR Journals paper as sole support.
4. **System architecture:** data → scout/simulator → scheduler → detector → evaluator → CSV/Streamlit.
5. **Experimental design:** matched budgets, paired clips/seeds, cue miss/false/delay conditions, event labels in the evaluator, and the disclosed oracle-derived cue path.
6. **Policy results:** three selected weak-label clips, matched quotas, MOG2 outcomes, and oracle-derived cue limitation.
7. **Detector comparison:** MOG2 versus clip-held-out ResNet probe at 25%, including false-positive frame counts and host runtime.
8. **Dataset and limits:** weak/manual labels, selected clip timing, IPAD exclusion, and no independent sensor evidence.
9. **Next steps and conclusion:** independently validate more events, obtain independent cues, add source-video groups, and evaluate physical sensors/edge hardware next semester.

Slides 10–12 carry the full 20-paper reference list and direct DOI links.

## Four-hour study plan

| Time | Focus | Output to rehearse |
|---|---|---|
| 00:00–00:35 | Understand the research question and scope boundaries | Explain what is measured versus simulated in one minute. |
| 00:35–01:20 | Trace the code path and four scheduler rules | Whiteboard the end-to-end pipeline and matched quota. |
| 01:20–02:00 | Learn the pilot metrics and synthetic evidence | Explain numerator/denominator, missed events, false-positive frame counts, latency units, and why three selected events cannot generalize. |
| 02:00–02:10 | Break | — |
| 02:10–02:55 | Review literature matrix and research gap | Summarize 3 strands and state the bounded gap without claiming novelty. |
| 02:55–03:25 | Dataset, license, annotations, and threats to validity | Explain why IPAD is not yet a validated local benchmark and name the fallback limits. |
| 03:25–03:50 | Practice likely viva questions aloud | Give concise answers below. |
| 03:50–04:00 | Final slide run-through and setup | Check filenames, citations, and evidence labels. |

## Likely viva questions and answers

**What is novel about SAGE?**  
We do not claim adaptive sampling itself is new. The project is a paired, reproducible comparison of four policies under matched frame budgets with a controlled analysis of simulated cue errors. Any empirical contribution is limited to validated data and conditions.

**Why simulate sensors instead of connecting hardware?**  
Simulation lets us vary misses, false triggers, and delay reproducibly before hardware integration. It tests sensitivity to those parameters, but does not establish real sensor accuracy or timing. Hardware is a next-semester extension.

**Are the simulated cues independent of ground truth?**  
No. Current cues are generated from annotated event starts. This is an oracle-derived controlled simulation and may overstate realistic cue knowledge. A future experiment should generate cues from a separately defined observable proxy or collect real sensor events.

**What does MOG2 detect?**  
Foreground change relative to an estimated background. It is sensitive to lighting, camera movement, shadows, and occlusion; it does not identify abnormal machine behavior.

**Why use HOG?**  
The installed OpenCV pedestrian detector is a readily available pretrained baseline for person presence. It is suitable only when labels mean people/workers. It is not a general industrial anomaly detector, so it is not a fair IPAD comparator unless labels support person detection.

**What is the pretrained ML comparator?**  
ImageNet-pretrained ResNet-18 produces frozen image scores; a class-balanced logistic head is trained on two selected clips' weak/manual normal/anomaly labels and tested on the third clip. Across three folds, its 25% event recall matched MOG2 while it produced fewer false-positive frames and took more host time. This is exploratory transfer learning on three clips, not an industrially validated anomaly model.

**How is fairness enforced?**  
Policies use the same clip, detector settings, cue realization, and exact frame quota. Labels remain in the evaluator. Scout runtime is charged to adaptive policies. We need to report current limitations, including oracle-derived cues and frame-wise rather than episode-wise false alarms.

**Why not say the project saves energy?**  
The budget is a modeled frame cap and runtime is measured on the current host. There is no power meter, edge deployment, or physical sensor, so energy savings are not measured.

**Why is IPAD not already used?**  
It is a good topical match, but its project page's website license does not license the videos. The mirror directs users to original sources for data terms. We have no local archive, verified source FPS, or evidence of annotation agreement. We cannot responsibly claim clearance or validation.

**What did the public-data pilot show?**  
Across three selected sequences with one weakly labeled interval each, fixed-rate sampling detected 3/3 events at 10%, 25%, and 50% budgets. Video-adaptive and budget-aware sampling detected 0/3 at 10% and 25%, and 1/3 at 50%. The ResNet probe showed the same event-recall pattern, with fewer false-positive frames at 25% and higher processing time than MOG2. Sensor-triggered sampling detected 3/3, but its cues came from event annotations, and deterministic fallback can detect events without cues. This small run cannot establish that cues improve performance.

**Can the conveyor dataset replace IPAD?**  
It supports a narrower lab-scale iron-ore foreign-object pilot under the Mendeley record's CC BY 4.0 listing. We checked frame mapping for three clips and ran one selected event interval per clip. Their labels are still weak/manual, and three selected events cannot replace a broader industrial video benchmark or establish annotation reliability.

**Are the timing and labels ground truth?**  
OpenCV reports 119.1829, 117.8108, and 119.3415 FPS for the selected clips. Five or six extracted frame IDs per clip match the decoded positions. This supports frame mapping but does not provide independent camera-clock accuracy. Pilot intervals come from consecutive normal/anomaly folder runs with unlabeled gaps omitted; label reliability remains unknown.

**Why is HOG's zero recall not evidence that it is worse?**  
HOG's pretrained weights detect pedestrians. The pilot labels describe foreign objects on a conveyor. The outputs do not measure the same target, so their scores are not directly comparable.

**What if sensor cues do not help?**  
That is a valid result. The project tests whether cue errors and budgets change the trade-off; a null or negative result informs whether physical integration is worth pursuing.

## Project paths to know

- `sage/engine.py`: experiment engine, cue simulation, detectors, schedulers, metrics, exports.
- `sage/cli.py`: command-line entry point.
- `app.py`: Streamlit result explorer.
- `docs/research/RESEARCH_GAP_AND_METHOD.md`: bounded research position and evaluation design.
- `docs/research/DATASET_VALIDATION.md`: current dataset evidence and unresolved gates.
- `docs/research/PUBLIC_DATA_PILOT.md`: exact pilot configuration, outcomes, and limits.
- `docs/IEEE_MANUSCRIPT_DRAFT.md`: IEEE-style study draft with actual pilot results and limitations.
