# SAGE research position and method

## Defensible research question

Prior work already studies adaptive video analytics, frame/configuration selection, edge resource allocation, and sensor-informed systems. SAGE should not claim invention of adaptive sampling or sensor-triggered analytics. Its defensible project question is narrower:

> Under a fixed analysis-frame budget and a stated industrial video/event definition, how do fixed-rate, video-activity, simulated sensor-cue, and combined budget-aware sampling compare in event coverage, false alarms, latency, and measured host processing time, and how sensitive are cue-guided policies to missed, false, and delayed cues?

This is a comparative software experiment. Generalization is limited to the data, labels, event rules, detector, and conditions actually evaluated. A contribution can be the reproducible paired comparison and explicit cue-error study, but only if public-data rights, event labels, and evaluation are validated first.

## Current hypotheses (testable, not assumed true)

- **H1:** At matched frame quota, cue-informed policies may improve event recall or latency over fixed-rate sampling when cue timing is informative.
- **H2:** Cue misses, false triggers, and delay may reduce or eliminate that benefit.
- **H3:** Video-only activity adaptation may match or outperform sensor-cue policies for visually observable events.

No hypothesis implies a positive result. The correct outcome may be no difference, a trade-off, or an inconclusive result.

## Variables and controls

| Category | Design |
|---|---|
| Independent variable | Sampling policy: fixed-rate, video-adaptive, sensor-triggered, budget-aware. |
| Controlled factors | Same ordered clip, event labels, detector, preprocessing, frame quota, and paired cue realization for each policy. |
| Cue factors | Event-cue detection probability, false-trigger rate, delay, and seed. State the cue generation mechanism as simulated/oracle-derived when generated from event starts. |
| Budget | Multiple predeclared frame fractions; compare policies at identical exact quota `ceil(N × fraction)`. |
| Outcomes | Event recall with hit/total, missed events, false-positive detections and a clearly named counting rule, latency with misses, analyzed frame count/fraction, scout/detector runtimes, and end-to-end host runtime if separately measured. |
| Unit of analysis | Clip and event; keep per-clip/per-event rows visible. Do not treat frames within a single clip as independent replicates. |

## Method to run after data validation

1. Freeze the dataset release, rights, clip list, anomaly/event definition, annotation-to-frame alignment, and source timing basis.
2. Partition by clip/device/process if any threshold or parameter is tuned. Keep a held-out evaluation set; never split adjacent frames randomly across tuning and evaluation.
3. Freeze detector parameters and ROI on calibration data. Current code has no ROI configuration or calibration workflow, so a full evaluation must add these or use a declared full-frame baseline and state that limitation.
4. For each held-out clip and budget, run all four policies on the same input and seed. Preserve raw configuration, frame traces, event rows, software versions, and failures.
5. Sweep cue reliability, false triggers, and delay using paired seeds; include a no-cue condition. Current cue generation starts from ground-truth event starts, so label this an oracle-derived controlled simulation, not independent sensor evidence.
6. Run pretrained detectors only for labels semantically supported by their outputs. OpenCV HOG's pretrained SVM detects pedestrians, so it is not comparable to conveyor contamination labels. The exploratory ResNet-18 linear probe uses binary normal/anomaly folder labels with a source-video-held-out split; report it as weak-label transfer learning, not an off-the-shelf anomaly detector.
7. Report per-clip and aggregate results with denominators, misses, timing units, exact frame quotas, and measured runtime methodology. With few clips, emphasize descriptive results; use clip-level paired uncertainty only when sample size supports it.

## Threats to validity to discuss

- **Cue oracle effect:** simulation cues derive from event annotations, which can give the sensor-guided policy unrealistically direct knowledge of event starts.
- **Model scope:** MOG2 is a motion/change detector and HOG is pedestrian detection. The ResNet-18 probe is trained on weak/manual labels and only tested on three held-out source clips; none of these results validates a general industrial anomaly detector.
- **Temporal labels:** the pilot converts one selected dense consecutive run per clip in the weak/manual anomaly-image folders into an event interval. This is a narrow operational rule, not independent event adjudication. Other clips contain gaps and partial labels.
- **Data scope and license:** the Mendeley record displays CC BY 4.0 and its archive subset has been inspected. The dataset is lab-scale and narrow. IPAD rights, timing, and annotation reliability remain pending.
- **Cost metric:** current runtime excludes decode/output; activity-adaptive policies incur a full-frame scout pass. Modeled frame budget is not measured edge capacity or energy.
- **False alarm metric:** current implementation counts each detector-positive frame outside labeled intervals, not merged alarm episodes. Name it accordingly; do not imply event-level alarm deduplication.
- **External validity:** one lab conveyor or a small set of selected industrial clips cannot establish deployment-wide performance.

## What can be claimed now

The software runs four policies at exact matched frame quotas and writes per-run, per-event, and per-frame outputs. Ten unit tests pass. Synthetic demonstrations and a five-condition cue ablation are recorded separately from the public-data runs. Three selected weakly labeled conveyor clips were evaluated at 10%, 25%, and 50% budgets with MOG2 and an ImageNet-pretrained ResNet-18 linear probe trained on the other two clips in each fold. Both detectors had the same event-recall pattern: fixed-rate 3/3 at each budget, video-adaptive/budget-aware 0/3 at 10% and 25%, and 1/3 at 50%. At 25%, the ResNet probe produced fewer false-positive frames at higher host processing time. These are exploratory outcomes from three selected events, not a validated industrial system or a general policy ranking. Cue-based policies are oracle-derived because event annotations seed the cue simulator. No physical sensor, edge-device, or energy claim has been verified. Elsevier's October 2026 source list confirms venue/source coverage for the cited publication years, but the exact article DOI records were not individually verified in Scopus.
