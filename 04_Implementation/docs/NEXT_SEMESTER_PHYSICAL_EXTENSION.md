# SAGE Next-Semester Physical Extension Plan

This plan describes future work. No physical sensor, microcontroller, camera trigger, Raspberry Pi, edge deployment, energy measurement, or field test is represented as completed by the v1.0 software study.

## Goal

Test whether real sensor signals can provide useful scheduling cues under controlled conditions, then measure the complete video pipeline on a selected edge computer. The experiment should preserve the v1.0 comparison so that simulation results can be compared with measured sensor behavior.

## Proposed staged work

### Stage 1 — Select and characterize the setup

- Choose one fixed-camera process and a narrowly defined set of observable events.
- Select a low-cost photoelectric/proximity sensor or vibration sensor based on the event physics; do not assume one signal generalizes across event types.
- Select a microcontroller/interface and an edge computer only after checking camera interface, I/O voltage, sampling rate, storage, and runtime support.
- Draw a system diagram and record component models, firmware/software versions, and safety constraints.

### Stage 2 — Bench-test the sensor path

- Collect synchronized ground truth and sensor output in a controlled, non-production setup.
- Measure true detections, misses, false triggers, timestamp error, communication delay, packet/data loss, and repeatability across trials.
- Test nuisance conditions relevant to the signal, such as distance, alignment, vibration, ambient light, or electrical noise.
- Estimate empirical cue-quality distributions; use these to replace or calibrate the v1.0 simulator parameters.

### Stage 3 — Integrate cue and video timing

- Establish a common clock or estimate clock offset/drift; record how timestamps are aligned.
- Buffer cues and video with explicit timeout and stale-cue behavior.
- Define safe fallback scheduling when the sensor or link is unavailable.
- Verify that labels remain evaluation-only and do not leak into policy decisions.

### Stage 4 — Edge deployment and measurement

- Deploy the same policy definitions and detector where supported.
- Measure CPU/GPU utilization, memory, throughput, dropped frames, temperature, and energy using a documented instrument/method.
- Separate idle, decode, inference, communication, and storage costs where feasible.
- Repeat runs and report device configuration, ambient/setup conditions, and measurement uncertainty.
- Do not transfer desktop timing directly to the edge device.

### Stage 5 — Deeper ML/DL anomaly subsystem

- First identify data with compatible event labels and sufficient process diversity.
- Establish simple baselines and determine whether labels support supervised, semi-supervised, or unsupervised learning.
- Compare an anomaly model against v1.0 classical CV and pretrained ML with matched clips, thresholds selected only on calibration data, and explicit compute/memory costs.
- Use temporal and device/process splits to avoid leakage; report false alarms per time and missed-event behavior, not only frame-level accuracy.
- Add this subsystem only with a research question that is feasible and meaningfully extends the sensor-guided scheduling study.

## Safety, privacy, and governance

- Keep early integration off live production equipment unless an approved risk assessment authorizes it.
- Use face-free framing, informed consent where people may be recorded, access control, retention limits, and institutional review as applicable.
- Do not connect a research prototype to machinery control or safety interlocks.
- Document failure modes and require human review before any operational interpretation.

## Exit criteria

- Reproducible sensor characterization with measured cue errors and delay.
- Verified clock alignment and documented fallback behavior.
- Paired comparison of all four policies under measured cues and controlled simulated conditions.
- Edge-resource measurements from the named device with repeatable method.
- Updated limitations and manuscript claims tied to evidence.

## Suggested student ownership

The project lead owns architecture, experimental design, integration, and paper consistency. Ravi and Rajarshi can own bounded work packages such as sensor bench characterization, dataset/annotation audit, or independent run reproduction, with review checkpoints. Coding assistants can help implement and review, but evidence and results should be checked by the project team.
