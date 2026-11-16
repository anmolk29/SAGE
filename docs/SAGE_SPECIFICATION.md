# SAGE v1.0 — Project Specification

**Full name:** Sensor-Guided Adaptive Video Processing for Resource-Constrained Industrial Monitoring  
**Version:** 1.0  
**Status:** Runnable software baseline and research protocol. Synthetic demo, automated tests, a bounded three-clip public-data pilot, and exploratory clip-held-out ResNet-18 linear-probe comparison pass. Broad public-dataset validation, independent sensor evidence, and deep anomaly-model evaluation remain future work.

## 1. Purpose and research question

SAGE studies whether simulated low-cost sensor cues help an industrial video monitor decide when to analyze frames, reducing processing effort without an unacceptable loss of event detection. The system is a reproducible software experiment and demonstrator. It does not establish physical sensor performance, edge-device energy use, or field reliability.

**Primary research question:** Under a stated video set, event definition, detector, and processing budget, do simulated sensor cues improve the trade-off between event coverage, false alarms, latency, and processing cost compared with fixed-rate and video-only adaptive sampling?

**Supporting questions:**

1. How do four scheduling policies compare under matched frame budgets?
2. How do missed, spurious, and delayed simulated cues affect sensor-guided policies?
3. Which conditions allow video-only adaptation to match or outperform cue-guided scheduling?
4. How do conclusions vary by clip and event type?

## 2. Scope and status boundaries

| Component | v1.0 status | Evidence required |
|---|---|---|
| Public industrial video | **A bounded three-clip Mendeley conveyor pilot is complete.** IPAD remains a candidate for future study; its archive is not local and its dataset-specific reuse terms and timing remain unresolved. | Broader clip inventory, label reliability, independent sensor evidence, and a semantically matched pretrained model |
| Video processing pipeline | **Implemented** for video files and ordered image folders; synthetic fixture is runnable. | Run trace with input identifier, frame count, parameters, and outputs |
| Classical CV baseline | **Implemented:** OpenCV MOG2 foreground/activity score. | Detector configuration and per-frame scores |
| Pretrained ML comparator | **Implemented and run:** ImageNet-pretrained ResNet-18 logits with a class-balanced logistic head trained on two selected clips and evaluated on the held-out third. HOG remains a pedestrian-only diagnostic. | Add more source-video groups and independently adjudicated anomaly labels; report model calibration and uncertainty |
| Region of interest | **Full-frame baseline only.** Dataset-specific ROI configuration and calibration are not yet in the CLI. | Record fixed ROI and calibration split where the selected clips require regional analysis |
| Sensor inputs | **Implemented as simulation:** seeded cues with misses, false triggers, and delay. No physical sensor data. | Seed, cue parameters, generated cue stream, and simulation label |
| Scheduling | **Implemented:** fixed-rate, video-activity-adaptive, sensor-triggered, and combined budget-aware policies, with a shared target frame quota and per-frame trace. | Per-frame scheduling trace and policy parameters |
| Resource results | **Implemented for software runs:** selected detector frames plus activity-scout time are recorded on the current host; target budget is modeled. Input decoding and output writing are excluded from detector runtime. | Host details, warm-up/repetition method, raw run records |
| Streamlit dashboard | **Implemented and smoke-run:** saved-result filtering, summary, comparison, event-type view, and CSV export; synthetic rows are called out. Streamlit 1.66.1 returned HTTP 200 on local startup. | Verify filtered exports against a larger real study dataset |
| Physical sensors / edge computer | Planned next-semester extension | Hardware plan and future validation; no v1.0 physical measurement claim |
| Deeper ML/DL anomaly detection | Planned research extension | Separate design and evaluation protocol |

Do not describe simulated cue values as sensor measurements. Distinguish measured host runtime from a modeled sampling/processing budget. Do not claim energy, Raspberry Pi performance, or industrial deployment without direct measurement.

## 3. Functional requirements

### Data and annotations

- Accept a documented public industrial video source and, where supported, an ordered image-frame sequence.
- **IPAD remains a future candidate:** *Industrial Process Anomaly Detection* (official project page: https://ljf1113.github.io/IPAD_VAD/; Hugging Face mirror: https://huggingface.co/datasets/MSherbinii/ipad-industrial-anomaly). Dataset-specific reuse terms, frame timing, and label reliability have not been verified, so IPAD is not used in the current pilot.
- Narrow subsets from three clips in the Mendeley iron-ore conveyor dataset (DOI 10.17632/s25x2bnshz.1) were retrieved and inspected. The record lists CC BY 4.0. Five or six sampled-frame indices per selected clip were checked against decoded video. Each pilot event uses weak/manual folder labels. See `docs/research/DATASET_VALIDATION.md` and `docs/research/PUBLIC_DATA_PILOT.md`; do not generalize these selected-clip checks to the entire dataset.
- Preserve provenance: dataset name, source page, license, access date, clip/device identifier, transformations, and relevant annotation source.
- Validate frame order and timing metadata before interpreting seconds or latency. If only ordered images are available, state the assumed replay rate and report latency in frames unless valid timing is known.
- Represent ground-truth events as clip-scoped intervals with event type and optional region of interest (ROI). The detector does not consume labels; the current event-derived cue simulator does. Explicitly label those sensor-guided conditions oracle-derived, and do not claim independent sensor evidence. A separate observable cue source is required for that claim.
- Record exclusions and missing/ambiguous annotations.

### Perception

- Run one interpretable classical-CV motion detector on frames selected by a scheduler.
- Run the built-in pretrained OpenCV HOG+linear-SVM pedestrian model for worker/person labels. An optional ONNX ResNet-18 ImageNet feature extractor with clip-held-out linear-probe heads is available for binary weak-label anomaly experiments. These small results do not establish a general industrial anomaly model. Model/head paths and runtime are recorded per run.
- Use a common clip, preprocessing policy, ROI convention, and evaluation labels for comparisons where the model supports the same event definition.
- Report model-specific limitations. A generic object detector is not evidence of semantic anomaly recognition; a motion detector reports motion rather than object identity or causal abnormality.

### Simulated cues

- Generate timestamped cues from a declared event/cue-generation rule.
- Expose detection probability (misses), false-trigger rate, and delay as parameters.
- Use deterministic random seeds; pair the same generated cue stream across policies in a comparison.
- Keep simulator inputs and generated cues separate from the ground-truth file consumed only by the evaluator.

### Scheduling policies

1. **Fixed-rate:** select uniformly spaced frame indices independent of activity and cues.
2. **Video-activity-adaptive:** prioritize current motion-scout activity while respecting the shared target frame quota.
3. **Sensor-triggered:** prioritize frames in a cue-active window while respecting the shared target frame quota.
4. **Budget-aware adaptive:** prioritize current motion activity or an arrived sensor cue, with a deterministic fallback cadence under the same quota.

All policies must log decisions and use identical detector settings. Every policy uses the same exact frame quota in a paired run; repeat the experiment at predeclared budget fractions for the trade-off curve.

### Experiment records and dashboard

- Save machine-readable run settings, software/model versions where available, seeds, clip IDs, policy, budget, cue condition, metrics, and per-clip outcomes.
- Dashboard filters: clip, policy, budget, cue reliability/false-trigger/delay condition, event type, and detector/model where available.
- Show event recall, missed events, false alarms, latency with misses clearly represented, processed frames/fraction, and measured software runtime.
- Show per-clip outcomes alongside aggregates; support export of the filtered records.
- Label measurements, simulations, and modeled constraints separately in the interface.

## 4. Metrics and definitions

- **Event recall:** number of annotated events with at least one valid detection divided by the number of annotated events. State the event-to-detection matching rule and report numerator/denominator.
- **False alarms:** current implementation counts each detector-positive analyzed frame outside annotated intervals. It does not merge repeated positives into alarm episodes. Name and report this rule; per clip-minute requires valid duration.
- **Detection latency:** timestamp of first valid detection minus event start. Report the distribution for detected events and separately count misses. Where timestamps are unavailable, report frames-to-detection and disclose any replay-rate assumption.
- **Processing cost:** selected detector-frame count/fraction and measured detector plus required activity-scout runtime on the named host. The common target frame budget is a modeled constraint. Decode, output writing, and dashboard runtime are excluded and must not be implied by the recorded processing time.
- **Trade-off:** event recall and latency versus processed frames and runtime, with matched-budget comparisons.
- **Optional uncertainty:** paired bootstrap intervals over clips or repetitions when sample size and design support it; do not imply population-wide generalization from a small convenience sample.

## 5. Reproducibility and fairness

- Freeze event definitions, ROI, detector settings, policy parameters, budget levels, cue conditions, and analysis plan before final evaluation.
- Split by clip/device/process, never randomly by adjacent frames, when tuning is performed.
- Use calibration clips for threshold selection and held-out evaluation clips for reported final comparisons.
- Apply identical clip sets, labels, preprocessing, and paired cue realizations across policies.
- Preserve all conditions, including failures and unfavorable outcomes; publish raw run-level tables where data rights allow.
- Record system environment and distinguish measured values from simulation parameters.

## 6. Non-functional requirements

- A clean setup must be documented with explicit dependency installation and run instructions.
- A small synthetic fixture must make smoke testing possible without downloading the full public dataset.
- Large datasets and model weights must not be committed to the repository; document retrieval and expected storage separately.
- Errors for unsupported codecs, missing model weights, invalid annotations, or absent optional dependencies must be actionable.
- Code and manuscript must not make unsupported performance, safety, novelty, or deployment claims.

## 7. Acceptance checklist

- [x] One Mendeley subset's provenance, displayed CC BY 4.0 terms, timing, sampled-frame mapping, labels, and limitations are documented. Dataset-wide label reliability remains unverified.
- [x] Classical CV and an ImageNet-pretrained ResNet-18 linear probe can be compared at matched frame budgets on the selected weak-label clips; HOG remains restricted to person/worker labels.
- [x] All four policies produce traceable schedules at the same exact frame quota.
- [x] Sensor miss, false-trigger, delay, and seed settings are recorded.
- [x] Metrics are defined, unit-checked, and computed from saved run records.
- [x] Matched-budget comparison and cue-quality ablations are represented.
- [x] Dashboard reads saved experiment outputs, filters event-level rows, and exports its current filtered view.
- [x] Automated tests and synthetic end-to-end smoke run pass.
- [x] Manuscript reports the bounded three-clip public-data pilot with its oracle-cue, weak-label, detector-semantics, and host-runtime limitations.
- [x] Future physical extension is separated from current software evidence.

## 8. Planned next-semester research extensions

1. Integrate a camera and low-cost photoelectric/proximity or vibration sensor through a microcontroller or edge interface.
2. Measure sensor accuracy, false triggers, timing/communication delay, power, and data loss under controlled conditions.
3. Deploy on a selected edge computer and measure CPU/GPU use, memory, throughput, thermal behavior, and energy with a stated method.
4. Expand the clip-held-out ResNet probe and, after validating labels, add deeper ML/DL anomaly detectors; compare their incremental value and cost against the classical baseline.
5. Conduct controlled tests before any live industrial use; document safety, privacy, consent, retention, and failure handling.

These items are planned work, not implemented v1.0 features.
