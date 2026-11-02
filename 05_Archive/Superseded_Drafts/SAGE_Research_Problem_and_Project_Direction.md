---
title: "SAGE: Research Problem, Evidence, and Project Direction"
project: "SAGE"
document_type: "Research and design review"
status: "Proposed direction — key decisions remain open"
last_updated: "2026-10-28"
---

# SAGE: Research Problem, Evidence, and Project Direction

## Purpose

This document assesses whether SAGE addresses a genuine engineering problem, identifies the current research basis, and outlines the evidence required to demonstrate that the proposed system provides value.

The project should be treated as a design review rather than as a commitment to a predetermined solution. The scope may need to be narrowed or changed if the literature, implementation constraints, or experimental results do not support the current direction.

## Executive summary

SAGE is considering a resource-aware video-processing system that adapts how frequently video frames are analyzed. The proposed investigation is whether sensor-event cues can help an edge-based video system decide when to allocate more computation.

The broader problem is credible: continuous video analysis can consume substantial processing resources, while reducing the sampling rate may increase detection latency or cause events to be missed. However, the existence of this broad problem does not establish that the proposed approach is novel or that it will outperform existing alternatives.

The current research review is preliminary. It has identified related work in edge video analytics, adaptive video processing, and camera observation scheduling, but it is not yet a systematic literature review and does not establish a specific research gap.

The recommended direction is to build a working engineering prototype and evaluate it rigorously. The project should compare fixed-rate sampling with activity-adaptive, sensor-triggered, and budget-aware policies using the same real video, documented event ground truth, and reproducible metrics. Sensor events may be simulated for controlled experiments, but results must be described as simulation-based unless physical sensors are tested.

**The project should be judged by the quality of its implementation and evidence, not by whether a particular algorithm wins or a paper is produced.**

## 1. Research status and existing work

### 1.1 Current status

Preliminary literature research has identified relevant work in three areas:

| Research area | Relevance to SAGE | Current implication |
|---|---|---|
| Edge video analytics | Examines the computational cost, latency, and analytical performance of processing video near its source. | Supports the relevance of resource-aware video processing and careful performance evaluation. |
| Adaptive video processing | Investigates changing frame-processing effort according to conditions or resource constraints. | Shows that adaptive processing is an established direction and cannot, by itself, be claimed as novel. |
| Camera observation scheduling | Treats when and where to observe as a scheduling problem. | Provides background for formulating observation and processing decisions as an algorithmic problem. |

Examples identified for further examination include:

- A 2023 survey on edge video analytics in *IEEE Communications Surveys & Tutorials*.
- *Adaptive Frame Sampling for Real-Time Video Object Detection and Multi-Object Tracking on Edge Devices*, reported as published online in June 2026.
- Work on active camera observation scheduling by Vaisenberg and colleagues (2009).
- *Towards Performance Clarity of Edge Video Analytics*, presented at the 2021 IEEE/ACM Symposium on Edge Computing.
- Work associated with *OsmoticGate* and *SplitStream* on adaptive edge video analytics and workload adaptation.

These references are starting points for the literature review, not proof of novelty. Their exact methods, experimental settings, limitations, and relevance to the proposed SAGE question must be examined in the original publications.

### 1.2 What can currently be claimed

The team can state that it has begun reviewing published research on edge video analytics, adaptive video processing, and observation scheduling. This initial review has helped define the problem area and highlighted the need to identify a narrower, evidence-based research question.

The team should not yet claim that:

- all relevant literature has been reviewed;
- no existing system addresses the problem;
- the proposed approach is the first of its kind;
- the proposed method is superior to existing approaches; or
- the project has established a research gap suitable for publication.

Those claims require further literature analysis and experimental evidence.

### 1.3 Next literature-review step

Create a literature matrix for the most relevant papers. For each paper, record:

- problem addressed;
- proposed method;
- hardware and deployment setting;
- datasets and experimental conditions;
- evaluation metrics;
- principal findings;
- stated limitations; and
- relevance to the specific SAGE research question.

The review should compare methods and limitations, rather than merely collecting citations that mention similar technologies. A defensible research gap can be stated only after this comparison.

## 2. Problem definition

### 2.1 The broader engineering problem

Continuous video analysis can be computationally expensive. Processing every frame at a high frequency may spend resources during periods when little relevant activity is occurring. Edge devices, including the Raspberry Pi, operate under finite computing and energy budgets.

Reducing the frequency of video analysis may reduce processing work, but it can also delay detection or cause events to be missed. The central trade-off involves:

- **Detection quality:** whether relevant events are detected.
- **Detection latency:** how quickly the system identifies an event.
- **Processing cost:** how many frames are processed and how much time processing consumes.
- **Resource constraints:** whether the workload fits within the chosen device or experimental budget.

Existing research supports the relevance of these trade-offs. It does not, by itself, establish that any particular SAGE design is necessary or effective.

### 2.2 The specific question SAGE could investigate

The proposed question is whether sensor-event cues can help a video-processing system decide when to allocate more computation.

For example, a fixed camera monitoring a controlled laboratory area might analyze frames less frequently while the scene is inactive, then increase its sampling rate when a sensor indicates that an event may be occurring.

This raises measurable questions:

- Can sensor-triggered sampling reduce processing work?
- Does it miss events that occur between sampled frames?
- Do noisy or delayed sensor signals cause unnecessary processing or late detection?
- Does the approach detect events quickly enough for the intended use case?
- Does it improve the trade-off compared with simpler video-only scheduling policies?

These questions should be tested rather than answered by assumption.

### 2.3 Proposed problem statement

> Resource-constrained edge devices may not be able to sustain continuous, high-frequency video analysis within a defined processing budget. This project will investigate whether adaptive video-sampling policies, including policies informed by sensor-event cues, can reduce video-processing cost while maintaining acceptable event-detection performance and latency. The policies will be evaluated against fixed-rate sampling using real video, controlled sensor simulations, documented ground truth, and reproducible benchmarks.

This statement defines a problem, a candidate approach, and criteria for evaluation without presuming that the proposed method will succeed.

### 2.4 Limits of the current approach

The current plan combines real video with simulated sensor signals. This enables controlled experiments with configurable sensor-event timing, noise, missed triggers, and delay. It does not establish the reliability of physical sensors in a real deployment.

Unless physical hardware is tested, the project must not claim to have validated a complete physical sensor-and-camera system. Similarly, a simulated processing budget is not equivalent to a measured performance result from a Raspberry Pi 4.

## 3. What would make the project credible?

A paper or dashboard alone is insufficient evidence that the problem has been solved. The implementation and experiments must demonstrate what the system actually does and under what conditions it is useful.

### 3.1 A working prototype

The prototype should:

1. load and process real video;
2. execute a documented computer-vision pipeline;
3. make frame-sampling decisions using selectable policies;
4. support configurable simulated sensor events and sensor imperfections;
5. record settings, detections, timing, and evaluation results; and
6. present results from actual experiment runs in a dashboard.

The dashboard must not rely on hard-coded numbers or present simulated performance as measured hardware performance.

### 3.2 Fair baseline comparison

At minimum, compare the following policies:

| Policy | Role in the evaluation |
|---|---|
| Fixed-rate sampling | Establishes a simple baseline for processing cost and detection performance. |
| Activity-adaptive sampling | Tests whether video-derived activity can guide the sampling frequency. |
| Sensor-triggered sampling | Tests whether simulated sensor cues add value to the scheduling decision. |
| Budget-aware adaptive sampling | Tests a policy that explicitly accounts for the available processing budget. |

All policies should use the same video clips, event definitions, ground-truth annotations, and evaluation procedure. Comparisons should report trade-offs across metrics rather than selecting only the metric that favors one policy.

### 3.3 Ground truth and event definitions

The project needs video clips with known event intervals. These may be controlled recordings annotated manually, provided the annotation rules are consistent and documented, or an appropriate dataset with suitable annotations.

Before evaluation, define:

- what constitutes an event in the selected application;
- when each event begins and ends;
- how a detection is matched to a ground-truth event;
- what time window or overlap rule determines a true positive; and
- how false positives, missed events, and duplicate detections are counted.

Without ground truth, the project can measure frame counts and processing time, but it cannot reliably determine event recall or whether detection performance is acceptable.

### 3.4 Metrics and success criteria

The evaluation should report, where applicable:

- frames processed;
- processing time and scheduling overhead;
- event precision and recall;
- missed and falsely detected events;
- detection latency; and
- performance under different sampling budgets and sensor-noise conditions.

Success criteria must be specified before the final experiments. For example, the team could test whether a policy reduces the number of processed frames while keeping event recall above a threshold justified by the selected application and baseline. The threshold must not be chosen after results are known merely to make the method appear successful.

A result in which sensor-triggered sampling reduces computation but misses too many events is still informative. So is a result in which activity-adaptive sampling performs similarly without requiring sensor cues. The aim is to produce a defensible answer, not to guarantee that the preferred method wins.

### 3.5 Evidence and claim boundaries

| Evidence collected | Claims it can support | Claims it cannot support on its own |
|---|---|---|
| Real video with simulated sensor events | Controlled comparison of scheduling policies under the stated simulation conditions. | Reliability of physical sensors in deployment. |
| Performance measurements on a Raspberry Pi 4 | Performance on that specific device under the tested conditions. | General performance across all edge devices. |
| Tests with a physical sensor and camera setup | Behavior of the integrated setup under the tested physical conditions. | Universal reliability or performance in all environments. |

Given the short project timeline, the team should not promise all three forms of evidence unless the required hardware tests can be completed and documented.

## 4. Defining the project's contribution

Two complementary directions are possible, but one should establish the primary objective.

### Option A: Engineering-system contribution

Build and evaluate a working resource-aware video-processing prototype. The system should demonstrate adaptive sampling, report measurable trade-offs, and document its operating limits.

The primary deliverable is a tested system with reproducible benchmarks and a clearly stated use case.

### Option B: Research-question contribution

Investigate whether sensor-event cues improve the trade-off between processing cost, detection quality, and latency compared with video-only adaptive sampling. Evaluate how noise, missed triggers, and delay affect the result.

The primary deliverable is a reproducible experiment that identifies when sensor cues help, when they do not, and under what conditions.

### Recommended approach

Use **Option A as the engineering foundation** and use the experiments to test the narrower question in Option B. This ensures that the project produces a functioning system while still evaluating whether its sensor-guided component provides measurable value.

The novelty risk remains significant: adaptive video analytics and frame sampling have already been studied. Combining a scheduler, OpenCV, and simulated sensor events is not sufficient by itself to establish a novel contribution.

A defensible contribution may instead be a carefully designed evaluation of sensor-cue reliability and scheduling performance under explicitly controlled constraints. Whether that contribution is sufficiently novel for a conference or journal remains unresolved until the literature review and experiments are complete.

## 5. Proposed response to the project review

The following points summarize the current position for discussion with the project supervisor.

### 5.1 Have we conducted research?

Preliminary research has begun in edge video analytics, adaptive video processing, and observation scheduling. Existing publications have been identified that examine the computational cost of video analytics and methods for adapting processing to changing workloads. This initial review also indicates that adaptive sampling is already an established area. The next step is to compare the relevant papers systematically and identify a specific question that is not adequately answered by existing work. The current review should not yet be described as comprehensive or systematic.

### 5.2 What problem are we solving?

The proposed problem is the computational cost of continuously processing video on resource-constrained edge devices. SAGE will investigate whether adaptive sampling can reduce unnecessary processing while maintaining acceptable event-detection performance and latency. The planned evaluation will compare fixed-rate sampling with activity-adaptive and sensor-triggered policies using real video and controlled experiments.

### 5.3 How will we demonstrate that the solution is credible?

The team will build a working prototype and compare the policies using the same video clips, documented ground truth, and reproducible evaluation criteria. The evaluation will measure processing cost, event-detection performance, and latency, and will test the effect of sensor noise and delay. Since sensor events are simulated in the current plan, conclusions will be limited to the conditions represented by the simulation. The objective is to deliver a functioning system and use experimental evidence to determine whether the proposed approach provides a measurable benefit.

## 6. Decisions required before implementation

The project scope should not be treated as final until the following questions are resolved.

### 6.1 Intended application and event definition

What concrete task will the video system perform—for example, detecting motion in a controlled laboratory area? The use case determines what counts as an event, what level of missed detection is acceptable, and how success should be measured.

### 6.2 Embedded Systems assessment requirements

Is simulation explicitly acceptable for the final assessment, or is at least one measurement on the Raspberry Pi or a physical sensor required? This determines whether the current simulation-led design satisfies the course requirements.

### 6.3 Primary project objective

Is the primary objective to demonstrate a practical, resource-aware video-processing system, or to investigate whether sensor cues improve adaptive scheduling? Both can be included, but the project must identify one as the main objective and align the implementation and evaluation around it.

### 6.4 Video and annotation availability

Are suitable video clips already available, or must the team obtain a public dataset or record its own clips? The selected clips must support a clear event definition and reliable ground-truth annotation.

The first decision is particularly important. Processing fewer frames does not automatically make a system better. The team must define what needs to be detected, why it matters, and what trade-off is acceptable before deciding whether the proposed approach is useful.

## 7. Immediate next steps

1. Select a concrete application and define the event to be detected.
2. Confirm whether the Embedded Systems assessment requires physical measurements or accepts simulation.
3. Identify suitable video clips and establish a ground-truth annotation procedure.
4. Read and compare the most relevant papers in a literature matrix.
5. Refine the research question based on the literature and assessment constraints.
6. Define the baseline policies, metrics, experimental conditions, and success criteria before running the final evaluation.
7. Freeze the scope only after these decisions are made.

## References for review

The following links were identified in the preliminary research notes. They should be checked against the original publications before being used as formal references in the report or paper.

1. *Towards Performance Clarity of Edge Video Analytics*, IEEE/ACM Symposium on Edge Computing, 2021. [IEEE Xplore record](https://ieeexplore.ieee.org/document/9708978/)
2. *OsmoticGate* / *SplitStream* related work on adaptive edge video analytics and workload adaptation. [IEEE Xplore record](https://ieeexplore.ieee.org/abstract/document/9839465/)
3. *Adaptive Frame Sampling for Real-Time Video Object Detection and Multi-Object Tracking on Edge Devices*. [Publisher page](https://gr-journals.com/journals/ictasa/issues/v2i2/26310)

Additional references mentioned in the preliminary review—a 2023 survey on edge video analytics and work on active camera observation scheduling by Vaisenberg and colleagues (2009)—must be identified and verified with complete bibliographic details before inclusion in a formal reference list.

---

**Current status:** The broad problem area is plausible and preliminary related work has been identified. The specific research gap, application, event definition, and required level of hardware validation remain open. The project should proceed to implementation only after these points have been resolved.
