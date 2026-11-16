# SAGE: A Reproducible Study of Sensor-Guided Adaptive Video Sampling for Industrial Monitoring

**Author(s):** [Complete author names and affiliations]  
**Manuscript status:** Protocol and results template. Replace bracketed fields only after verified experiments. No result values or conclusions are asserted in this draft.

## Abstract

Industrial video analytics can consume substantial compute when every frame is analyzed, while resource-constrained monitoring systems must balance event coverage, response time, and processing cost. This paper presents SAGE, a software framework for evaluating whether simulated sensor-event cues help schedule video analysis. The protocol compares fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware adaptive policies using a shared video pipeline, a classical computer-vision baseline, and one documented pretrained machine-learning comparator. A configurable cue simulator represents missed triggers, false triggers, and delay. The evaluation measures event recall, false alarms, detection latency, analyzed-frame count, and host software runtime across matched budgets and cue-quality conditions. Ground-truth annotations are isolated from scheduling decisions, and runs record their settings and random seeds. The study uses [dataset and version; license and temporal representation to be verified] and reports [clip/event counts after evaluation]. Physical sensors and edge-device energy measurements are outside the current study. The final paper will report whether simulated cues add value under the tested conditions, including negative results and limitations; no general deployment or novelty claim is made in advance.

**Index Terms—** edge video analytics, industrial monitoring, adaptive sampling, event-triggered processing, sensor simulation, resource-aware scheduling.

## I. Introduction

Video monitoring can be computationally wasteful when a detector processes every frame during long quiet periods. Edge-video analytics research has studied query optimization, resource allocation, placement, and adaptive processing; adaptive sampling alone is therefore not the claimed novelty of SAGE [1]–[5]. This work addresses a narrower empirical question: under a fixed event definition and analysis budget, do imperfect sensor cues improve frame scheduling beyond fixed-rate and video-only adaptation?

SAGE combines real industrial video, a transparent classical-CV detector, one pretrained ML comparator, configurable simulated sensor cues, four scheduling policies, and a reproducible evaluation interface. The software is intended to test trade-offs, not to validate a physical sensor or claim edge-device energy performance.

This paper makes the following bounded contributions, subject to completion of the experiment:

1. An implementable protocol for paired comparison of four frame-scheduling policies.
2. A cue simulator that exposes misses, false triggers, delay, and reproducible random seeds.
3. A run-record format and dashboard for inspecting per-clip and aggregate results.
4. An empirical characterization of the tested clips and conditions, to be completed after runs and reported with limitations.

## II. Research Questions

- **RQ1:** At matched analysis budgets, how do fixed-rate, video-only adaptive, sensor-triggered, and budget-aware adaptive policies compare on event recall, false alarms, latency, and processing cost?
- **RQ2:** How do simulated cue misses, false triggers, and delays change the performance of sensor-guided policies?
- **RQ3:** Under which tested conditions does video-only adaptation match or outperform sensor-guided scheduling?

The protocol does not presume a positive outcome. A finding that cues add no benefit, or that cue errors erase their benefit, remains informative for deciding whether physical sensor integration is justified.

## III. Related Work

Edge-video analytics surveys describe applications, architectures, enabling techniques, and open systems challenges [1]. NoScope uses video-specific cascades to reduce query cost [2]. VideoEdge studies query plans and placement under quality and resource constraints [3]. Yoda emphasizes variation in video analytics performance across videos and time, motivating per-clip and paired evaluation [4]. OsmoticGate explores adaptive edge-based real-time analytics [5]. These works place SAGE within established resource-aware video analytics. The literature review is a structured starting map, not a completed systematic review; any formal gap or novelty claim requires an updated search and supervisor review.

## IV. System and Experimental Method

### A. Data and ground truth

The current public candidate is IPAD, *Industrial Process Anomaly Detection* (official project page: https://ljf1113.github.io/IPAD_VAD/; Hugging Face mirror: https://huggingface.co/datasets/MSherbinii/ipad-industrial-anomaly). Project research previously recorded an approximately 8.92 GB mirror-card size; this is not a verified current download measurement. The present workspace does not contain the dataset. Before final evaluation, verify the current release contents and license conditions with the original source and document whether material is playable video or ordered image frames, how frame order is established, whether timestamps/frame rate are available, and how annotations map to events. If original timing cannot be established, latency will be reported in frames; any replay-rate assumption will be stated and will not be presented as original event timing.

Each clip is represented by an identifier and event intervals containing [start, end, event type, ROI]. The scheduler and detector must not read ground-truth labels. Any calibration/evaluation split is performed by clip or device/process rather than adjacent frames. Dataset permissions, exclusions, transformations, privacy constraints, and annotation provenance will be reported.

### B. Perception methods

The implemented classical-CV baseline uses OpenCV MOG2 background subtraction on 320 × 240 grayscale scout frames (`history=120`, `varThreshold=32`, shadows disabled, learning rate 0.1 during the first four frames and 0.01 thereafter). The foreground-pixel fraction is the activity score; the configurable default threshold is 0.015. This detects visual change, not semantic abnormality or causality. The present baseline has no ROI-specific scoring or calibration/held-out threshold workflow; those settings must be frozen and reported for a dataset evaluation.

The implemented pretrained comparator is OpenCV's built-in default HOG descriptor with its pretrained linear-SVM pedestrian weights (`cv2.HOGDescriptor_getDefaultPeopleDetector()`), distributed through the installed OpenCV package. Frames are resized to 640 pixels wide and evaluated with 8 × 8 stride, 8 × 8 padding, and scale 1.05. It detects pedestrian/person presence only; it is not a general industrial anomaly or machinery detector. Compare its output with the motion baseline only on the same worker/person event labels. The selected OpenCV version is written into each result row. No real-data HOG-versus-motion result is claimed until a suitable labeled clip is supplied and evaluated.

### C. Simulated sensor cues

The simulator transforms [declared event or signal-generation rule] into timestamped cues with detection probability [levels], false-trigger rate [levels], and delay [levels]. It uses random seed [seed policy]. Each policy in a paired comparison receives the same cue realization. The annotations remain evaluation-only inputs. These synthetic cues test sensitivity to controlled error and do not estimate physical sensor accuracy, placement, or communication behavior.

### D. Scheduling policies

1. **Fixed-rate:** uniformly spread a target quota across the clip, independent of visual activity and cues.
2. **Video-activity-adaptive:** prioritize frames whose current lightweight motion-scout score exceeds a threshold, with a deterministic fallback cadence to fill the shared quota.
3. **Sensor-triggered:** prioritize frames in an already-active simulated-cue window, with a deterministic fallback cadence to fill the shared quota.
4. **Budget-aware adaptive:** prioritize a frame when current visual activity or an already-arrived cue is present, with deterministic fallback under the same quota.

All policies share decoding, preprocessing, detector parameters, and evaluation clips. Each policy analyzes an exact common quota of `ceil(frame_count × budget_fraction)` frames; the quota is repeated at each predeclared budget fraction. The video-activity and budget-aware policies also scan each frame with the lightweight scout. Its measured time is charged to those policies; `processing_time_seconds` excludes media decoding, scheduler overhead, and output writing. Policy-specific parameters and per-frame decision traces are retained. The current CLI uses full-frame motion scores and does not yet configure per-clip regions of interest.

### E. Metrics

- Event recall is detected annotated events divided by all annotated events, with the matching rule and counts stated.
- False alarms are detections outside annotated intervals, reported as a count and per clip-minute when clip duration is valid.
- Latency is first valid detection time minus event start. Misses are reported separately; where original timestamps are unavailable, latency is in frames.
- Processing cost includes analyzed frame count/fraction and measured software runtime on a named machine. Modeled budget limits are identified separately.
- Trade-off plots show recall and latency against analyzed frames and measured runtime.

### F. Experimental matrix and analysis

| Factor | Planned comparison levels | Control/reporting rule |
|---|---|---|
| Policy | Four policies | Same clips and detector; matched budgets |
| Frame budget | [predeclare low, medium, high fractions; `--budget` sets the fraction] | Each policy analyzes exactly `ceil(total frames × fraction)` frames |
| Cue detection | [reliable, moderate, degraded] | Exact probabilities and seeds logged |
| False triggers | [low, elevated] | Rate denominator and generated cue stream logged |
| Delay | [immediate, delayed] | Frames or seconds, consistent with source timing |
| Clip condition | [quiet, intermittent, short/long events] | Per-clip outcomes shown |
| Detector | Classical CV and pretrained model | Model provenance and event compatibility reported |

Primary comparisons are paired by clip, budget, cue realization, and repetition seed. Report per-clip data and aggregate median with spread. If supported by the sample design, calculate paired bootstrap intervals at the clip level. No condition or metric will be omitted solely because it is unfavorable. A predeclared analysis plan and all parameter values will accompany final results.

## V. Implementation and Reproducibility

The implementation comprises [module names/commit], a command-line or equivalent experiment entry point [command], machine-readable run records [schema], and a Streamlit dashboard [launch command]. A small fixture permits an end-to-end smoke test without downloading the full public dataset. Exact software versions, operating system, CPU/GPU where relevant, warm-up procedure, repetitions, and runtime measurement method will be recorded. The dashboard is a means to inspect experiment outputs; it is not independent evidence of performance.

## VI. Results

**Do not complete this section with anticipated or synthetic values.** Import results from verified runs and state the exact dataset subset and code/configuration used.

### A. Dataset and run coverage

| Item | Value to fill from run manifest |
|---|---|
| Dataset/release/license | [ ] |
| Clips / events / event types | [ ] |
| Timing source or replay assumption | [ ] |
| Evaluation split | [ ] |
| Policies, budgets, cue settings, seeds completed | [ ] |
| Host and software environment | [ ] |

### B. Primary policy comparison

[Insert a table with each policy and matched budget: event recall (numerator/denominator), false alarms, median detected-event latency plus misses, analyzed frames, and measured runtime. Include per-clip variability and confidence intervals if computed.]

### C. Cue-quality and ablation results

[Report how performance changes with misses, false triggers, and delays. Include video-only, no-cue, cue-only, and combined ablations if run. Keep simulator parameters visible.]

### D. Classical CV and pretrained model comparison

[Report model provenance, compatible event labels, metrics, processing cost, failures, and runtime. Explain any non-equivalent output semantics.]

## VII. Discussion

[Interpret only observed results.] Discuss whether sensor cues changed the recall/cost/latency trade-off under the tested conditions, where they failed, how outcomes varied by clip, and whether video-only adaptation was competitive. Relate findings cautiously to prior resource-aware analytics; avoid broad claims from a small dataset.

## VIII. Limitations, Ethics, and Future Work

Simulation does not validate physical sensor detection, false-trigger rates, timing, placement, communication, or integration. Host runtime is not an edge-device or energy measurement. Motion detectors are sensitive to camera movement, lighting, shadows, and occlusion; a pretrained model is bounded by its classes and training domain. Dataset temporal representation and annotation quality constrain latency and event claims. A small selected clip set supports conclusions only for the tested conditions. The literature map is not a systematic review.

Use public data only under documented terms. Do not store identifiable face imagery; avoid face recognition. For any new recordings, obtain consent and follow institutional review and retention requirements. Next-semester work may add physical sensors and edge deployment, followed by deeper ML/DL anomaly detection if compatible data and a clear incremental research question are available.

## IX. Conclusion

[Write after the complete experiment.] Summarize what the evidence supports for the tested dataset, conditions, and measured software pipeline. Clearly state whether cue guidance helped, failed, or was inconclusive. Do not claim physical deployment, energy savings, safety efficacy, or a field-wide research gap without corresponding evidence.

## References

[1] R. Xu, S. N. Razavi, and R. Zheng, “Edge Video Analytics: A Survey on Applications, Systems and Enabling Techniques,” *IEEE Communications Surveys & Tutorials*, vol. 25, pp. 2951–2982, 2023, doi: 10.1109/COMST.2023.3323091.

[2] D. Kang, J. Emmons, F. Abuzaid, P. Bailis, and M. Zaharia, “NoScope: Optimizing Neural Network Queries over Video at Scale,” *Proceedings of the VLDB Endowment*, vol. 10, no. 11, pp. 1586–1597, 2017, doi: 10.14778/3137628.3137664.

[3] C.-C. Hung et al., “VideoEdge: Processing Camera Streams using Hierarchical Clusters,” in *Proceedings of the 2018 IEEE/ACM Symposium on Edge Computing*, 2018, doi: 10.1109/SEC.2018.00016.

[4] Z. Xiao, Z. Xia, H. Zheng, B. Y. Zhao, and J. Jiang, “Towards Performance Clarity of Edge Video Analytics,” in *Proceedings of the Sixth ACM/IEEE Symposium on Edge Computing*, 2021, doi: 10.1145/3453142.3491272.

[5] B. Qian, Z. Wen, J. Tang, Y. Yuan, A. Y. Zomaya, and R. Ranjan, “OsmoticGate: Adaptive Edge-Based Real-Time Video Analytics for the Internet of Things,” *IEEE Transactions on Computers*, vol. 72, no. 4, pp. 1178–1193, 2023, doi: 10.1109/TC.2022.3193630.

[6] OpenCV, “How to Use Background Subtraction Methods,” *OpenCV Tutorials*. Available: https://docs.opencv.org/4.11.0/d1/dc5/tutorial_background_subtraction.html. Accessed: [verify access date].
