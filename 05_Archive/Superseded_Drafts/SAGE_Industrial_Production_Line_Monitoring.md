---
title: "SAGE: Industrial Production-Line Monitoring — Application and Scope Refinement"
project: "SAGE"
document_type: "Project application and research-scope refinement"
status: "Proposed direction — pending footage and assessment confirmation"
last_updated: "2026-10-31"
---

# SAGE: Industrial Production-Line Monitoring
## Application and Research-Scope Refinement

## 1. Purpose

This document refines the proposed application of SAGE around industrial production-line monitoring. It establishes the practical motivation, proposed system behavior, research question, evaluation requirements, scope boundaries, and decisions that must be resolved before implementation.

The proposed direction is to investigate whether adaptive video analytics can reduce unnecessary computational work in visual monitoring while maintaining acceptable event-detection performance and latency.

SAGE is a monitoring and resource-allocation project. It is not an industrial robot-control system, a factory-wide automation platform, or a replacement for established industrial safety systems.

## 2. Application: industrial production-line monitoring

Industrial production-line monitoring provides a concrete setting in which cameras, sensors, and automated equipment are used to observe production processes.

The initial application is narrowed to a **manufacturing conveyor line**. The system will monitor visual activity and operational interruptions in a defined area of the line.

Candidate events include:

- Conveyor stoppages.
- Unexpected gaps in material flow.
- Accumulation of products.
- Production activity falling below an expected level.
- An object failing to appear at an expected monitoring station.

These are candidate event categories, not a finalized event taxonomy. The team must select a manageable subset and define each event precisely before creating annotations or evaluating detection performance.

## 3. Problem definition

### 3.1 Engineering problem

Continuous visual monitoring can require substantial computation, particularly when video frames are analyzed at a high frequency. However, intensive analysis may not be necessary at every moment. During periods of normal or low activity, processing every frame may use resources without providing a corresponding improvement in monitoring value.

Reducing the frequency of visual analysis can lower processing work, but it may also delay the detection of important events or cause events to be missed.

The engineering problem is therefore a resource-allocation trade-off:

- allocate enough processing to detect relevant production events;
- avoid unnecessary frame analysis when intensive processing is not needed;
- maintain acceptable event-detection accuracy and latency; and
- operate within a defined computational budget.

The potential business relevance is more efficient use of computing resources for visual monitoring. Any financial benefit must be estimated from measured resource savings and deployment costs. SAGE will not directly demonstrate increased manufacturing profits or improved robot productivity.

### 3.2 Proposed problem statement

> Continuous visual monitoring of industrial production lines can impose computational overhead, even during periods when intensive video analysis may not be necessary. This project will investigate whether adaptive video-processing policies, including policies informed by sensor-event cues, can reduce computational overhead while maintaining acceptable event-detection accuracy and latency under varying operating conditions.

### 3.3 Proposed research question

> Can sensor-guided adaptive video processing reduce computational overhead in industrial production-line monitoring while maintaining acceptable event-detection accuracy and latency under varying operating conditions?

This question is deliberately open-ended. The experiments must determine whether sensor guidance provides a measurable benefit compared with fixed-rate and video-only adaptive processing.

## 4. Proposed SAGE system

The proposed system will combine production-line video, a computer-vision pipeline, a sensor-event simulator, an adaptive scheduling engine, and an experiment dashboard.

### 4.1 System workflow

```text
                 Production-line video
                          |
                          v
                Computer-vision pipeline
                          |
             Visual activity / event cues
                          |
                          v
                 Adaptive scheduler
                          ^
                          |
                 Sensor-event simulator
                          |
                          v
                Sampling-rate decision
                          |
                          v
                Selected video frames
                          |
                          v
                 Event detection
                          |
                          v
                 Experiment logger
                          |
                          v
              Metrics, comparisons, results
                          |
                          v
                Monitoring dashboard
```

The workflow is conceptual. The final architecture and interfaces will be determined during implementation planning.

### 4.2 Video input and computer vision

The system will process real video of a production-line environment. The computer-vision component will identify visual activity relevant to the selected event categories.

The exact processing pipeline and event-detection method must be selected after the team reviews the available footage. The implementation should use documented image-processing or computer-vision operations and should not claim to detect events that cannot be reliably distinguished in the selected clips.

### 4.3 Sensor-event simulation

The initial design may use simulated proximity or photoelectric sensor events to represent signals that could be available near a conveyor or monitoring station.

The simulator should support controlled variations such as:

- event timing;
- false-positive triggers;
- missed triggers; and
- signal delay.

Simulated signals allow repeatable experiments, but they are not physical sensor measurements. Results based on them must be reported as simulation-based.

### 4.4 Adaptive scheduling engine

The scheduling engine will decide when and how frequently video frames should be processed. For example:

- when the system has no indication of activity, it may reduce the processing frequency;
- when a sensor cue indicates that an object may have entered a monitoring zone, it may temporarily increase the processing frequency; and
- when activity returns to a stable state, it may reduce the processing frequency again.

These are proposed behaviors. Their effectiveness must be measured, particularly when sensor signals are noisy, delayed, or missed.

### 4.5 Monitoring dashboard

The dashboard should display results generated by actual experiment runs, including:

- detected events;
- processing frequency and frames processed;
- processing-time measurements;
- detection accuracy;
- detection latency; and
- comparisons between scheduling policies.

The dashboard must not use hard-coded values presented as experimental results.

## 5. Experimental comparison

To determine whether adaptive scheduling provides value, SAGE should compare multiple policies using the same video clips, event definitions, ground-truth annotations, and evaluation procedure.

| Policy | Description | Evaluation purpose |
|---|---|---|
| Fixed-rate sampling | Processes frames at a constant interval. | Baseline for detection performance and processing cost. |
| Activity-adaptive sampling | Adjusts sampling frequency using activity inferred from video. | Tests whether video-derived activity can guide processing allocation. |
| Sensor-triggered sampling | Uses sensor-event cues to adjust sampling frequency. | Tests whether sensor cues add value to the scheduling decision. |
| Budget-aware adaptive sampling | Adjusts processing decisions while accounting for a defined computational budget. | Tests behavior under explicit resource constraints. |

Each policy should be tested on equivalent inputs and under documented parameter settings. Results should report trade-offs rather than relying on a single metric.

## 6. Evaluation methodology

### 6.1 Ground truth and event definitions

Before the experiments, the team must define:

1. which production-line events are in scope;
2. how the start and end of each event will be identified;
3. how video segments will be annotated;
4. how a system detection will be matched to a ground-truth event; and
5. how false positives, missed events, and duplicate detections will be counted.

Suitable footage must contain enough examples of the selected events to support meaningful evaluation. If a clip shows only normal operation, it cannot by itself establish event-detection performance for interruptions.

### 6.2 Metrics

The evaluation should report, where applicable:

- event precision and recall;
- missed-event and false-positive counts;
- detection latency;
- number of frames processed;
- total processing time;
- scheduling overhead; and
- performance under different sampling budgets and sensor-simulation conditions.

If actual device measurements are collected, the device model, software environment, video settings, and test conditions must be documented.

### 6.3 Success criteria

Success criteria should be defined before the final evaluation. A possible criterion is to determine whether a policy reduces the number of processed frames while maintaining event recall and detection latency within application-appropriate limits.

The team must justify any thresholds based on the selected use case and baseline. Thresholds should not be selected retrospectively to make a preferred policy appear successful.

A negative or inconclusive result is acceptable if the methodology is sound. For example, the experiments may show that video-only adaptive sampling performs as well as sensor-guided sampling, or that sensor noise eliminates the expected benefit. Such findings should be reported accurately.

## 7. Potential business relevance and claim boundaries

### 7.1 Potential value

If adaptive processing reduces unnecessary computation while preserving acceptable monitoring performance, possible deployment benefits could include:

1. reduced video-processing workload;
2. potentially lower CPU utilization and energy consumption;
3. more efficient use of edge-computing hardware; and
4. potentially lower operating costs when similar monitoring stations are deployed at scale.

These are potential benefits, not outcomes established by the project.

### 7.2 Economic claims

SAGE should first measure technical resource savings. Any financial estimate would require additional information, including:

- measured changes in processing workload;
- energy consumption and applicable electricity costs;
- hardware acquisition or upgrade costs;
- deployment and integration costs;
- maintenance costs; and
- the number of monitoring stations over which savings might scale.

The project should not claim increased factory profits or a quantified return on investment without this analysis.

### 7.3 Explicit limitations

SAGE will not, within its initial scope:

- control industrial robots or conveyor machinery;
- replace industrial safety systems;
- claim to prevent manufacturing accidents;
- attempt complete factory-wide automation;
- require access to operational industrial machinery; or
- claim physical sensor integration when sensor inputs are simulated.

The project investigates adaptive visual monitoring and computational resource allocation.

## 8. Footage and data requirements

Access to suitable footage is a critical dependency. A convincing industrial-monitoring demonstration requires footage that genuinely depicts a production-line environment and supports the selected event definitions.

### 8.1 Preferred source

The team should first determine whether suitable footage is available through an industrial or IoT-related contact, including the project team's existing professional connections. No access should be assumed until the source confirms availability and permission.

### 8.2 Required footage characteristics

Ideally, footage should include:

- a conveyor or production-line environment;
- a stable and interpretable camera view;
- normal production activity;
- one or more relevant interruptions or irregularities;
- sufficient duration to test both normal and event periods; and
- adequate visual quality for the selected detection method.

The team should establish whether the footage may be used for academic research, stored in the project repository, shown in a demonstration, and included in a paper or presentation. Permission for one use does not automatically imply permission for all uses.

### 8.3 If industrial footage is unavailable

The team should not describe generic footage as industrial footage. It should instead evaluate the available alternatives:

- identify a suitable public industrial dataset;
- obtain permission to record or use representative production-line footage; or
- revise the application claim to match the actual data.

Any change in dataset or application must be reflected in the problem statement, methodology, and limitations.

## 9. Scope boundaries and dependencies

| Area | Proposed position | Status |
|---|---|---|
| Application | Conveyor-based industrial production-line monitoring | Proposed |
| Video | Real production-line footage | Availability unconfirmed |
| Computer vision | Visual activity and selected operational-event detection | Method to be finalized |
| Sensor input | Simulated proximity or photoelectric sensor events | Proposed |
| Scheduling | Fixed-rate, activity-adaptive, sensor-triggered, and budget-aware policies | Proposed comparison |
| Dashboard | Displays actual experiment outputs and policy comparisons | Proposed |
| Physical machinery control | Excluded | Out of scope |
| Physical sensor validation | Not assumed in the initial simulation-led design | Requires assessment confirmation |
| Hardware benchmarking | Only claim measurements actually collected on the named device | Conditional |
| Economic analysis | Estimate only if measured savings and cost inputs are available | Optional extension |

## 10. Decisions required before scope freeze

### D1. Industrial footage availability

- Is actual manufacturing-line footage available?
- Does it contain normal operation and relevant interruptions?
- Is the team permitted to use it for academic evaluation, demonstrations, and publication?

### D2. Event selection

- Which one or two event categories will be the initial focus?
- Can those events be identified consistently in the available footage?
- Can reliable ground-truth annotations be created?

### D3. Embedded Systems requirements

- Does the assessment accept simulation?
- Is a Raspberry Pi demonstration or physical sensor measurement compulsory?
- Are there required embedded techniques or artifacts that must be demonstrated?

### D4. Sensor strategy

- Will sensor events remain simulated for the initial evaluation?
- If physical sensors are required, which sensor and measurement setup are feasible within the project timeline?

### D5. Experimental scope

- Which sampling policies can be implemented and evaluated reliably?
- What computational budgets and sensor-noise conditions will be tested?
- What detection-performance and latency thresholds are appropriate for the selected application?

### D6. Research contribution

- Does the literature comparison support a specific unresolved question about sensor-guided scheduling?
- Is the intended contribution primarily an evaluated engineering system, an experimental comparison, or both?

## 11. Recommended next steps

1. Confirm whether suitable industrial footage can be obtained and used.
2. Confirm the Embedded Systems assessment requirements, particularly whether physical measurements are mandatory.
3. Select a small number of observable production-line events.
4. Check that the available footage supports those events and can be annotated.
5. Complete a focused comparison of related research on edge video analytics, adaptive frame sampling, and observation scheduling.
6. Finalize the baseline policies, metrics, and experimental conditions.
7. Freeze the scope and prepare the implementation plan.

The project should not begin with an assumption that sensor-guided sampling will outperform the alternatives. The purpose of the experiment is to establish whether it does, under which conditions, and at what computational and detection-performance trade-off.

## 12. Current project position

The proposed application is **industrial production-line monitoring, narrowed to a conveyor-line environment**. The proposed research investigates whether sensor-guided adaptive video processing can reduce computational overhead while maintaining acceptable event-detection accuracy and latency.

The direction has a plausible practical motivation, but the final scope is not yet fully validated. Industrial footage availability, event definitions, hardware-assessment requirements, and the specific research contribution remain open.

The next scope decision should be based on those constraints rather than on the preferred implementation alone.
