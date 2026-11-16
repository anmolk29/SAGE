# SAGE: A Reproducible Study of Sensor-Guided Adaptive Video Sampling for Industrial Monitoring

**Authors:** Anmol Kapila (Roll No. 2428020219), Ravi Bansal (Roll No. 2428020189), Rajarshi Aggarwal (Roll No. 2428020188).  
**Manuscript status:** IEEE-style study draft with descriptive results from three selected weak-label clips and an exploratory clip-held-out ResNet-18 linear probe. Author affiliations and any institution-specific formatting remain to be supplied by the project team.

## Abstract

Industrial video analytics can consume substantial compute when every frame is analyzed, while resource-constrained monitoring systems must balance event coverage, response time, and processing cost. SAGE compares fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware scheduling at matched analysis quotas. This draft reports three weakly labeled transitions from a public lab-scale iron-ore conveyor dataset. A frozen ImageNet-pretrained ResNet-18 feature extractor and class-balanced logistic head, trained on two clips and evaluated on the held-out third, matched MOG2 event recall at each tested budget. At 25%, the ResNet probe yielded fewer false-positive frames (25/38/22/38 versus 73/128/59/128 for fixed/video/sensor/budget policies) but required more measured host processing time (2.891 versus 0.736 seconds summed for fixed-rate). The three-event results are exploratory and do not establish general anomaly-detection accuracy, sensor benefit, edge savings, or energy savings.

**Index Terms—** edge video analytics, industrial monitoring, adaptive sampling, event-triggered processing, sensor simulation, resource-aware scheduling.

## I. Introduction

Video monitoring can be computationally wasteful when a detector processes every frame during long quiet periods. Edge-video analytics research has studied query optimization, resource allocation, placement, and adaptive processing; adaptive sampling alone is therefore not the claimed novelty of SAGE [1]–[5]. This work addresses a narrower empirical question: under a fixed event definition and analysis budget, do imperfect sensor cues improve frame scheduling beyond fixed-rate and video-only adaptation?

SAGE combines public lab-scale conveyor video, a classical-CV activity detector, an exploratory pretrained ResNet-18 linear probe, configurable simulated sensor cues, four scheduling policies, and a reproducible evaluation interface. The software tests trade-offs; it does not validate physical sensors or edge-device energy performance.

This paper makes the following bounded contributions:

1. An implementable protocol for paired comparison of four frame-scheduling policies.
2. A cue simulator that exposes misses, false triggers, delay, and reproducible random seeds.
3. A run-record format and dashboard for inspecting per-clip and aggregate results.
4. A clip-held-out exploratory ResNet-18 comparison and an openly qualified three-clip policy characterization, including misses by video-adaptive policies and limits that prevent broader claims.

## II. Research Questions

- **RQ1:** At matched analysis budgets, how do fixed-rate, video-only adaptive, sensor-triggered, and budget-aware adaptive policies compare on event recall, false alarms, latency, and processing cost?
- **RQ2:** How do simulated cue misses, false triggers, and delays change the performance of sensor-guided policies?
- **RQ3:** Under which tested conditions does video-only adaptation match or outperform sensor-guided scheduling?

The protocol does not presume a positive outcome. A finding that cues add no benefit, or that cue errors erase their benefit, remains informative for deciding whether physical sensor integration is justified. In the current implementation, event annotations seed the cue simulator; this is an oracle-derived controlled condition, not independent sensor evidence.

## III. Related Work

Edge-video analytics surveys and systems have studied architecture, filtering, sampling configuration, query scheduling, bandwidth allocation, and edge/cloud placement [1]–[6], [19], [20]. Reducto's on-camera filtering and IEEE work on adaptive rate/configuration selection establish strong prior art; adaptive sampling is not a SAGE novelty claim [2], [6]. MACEdge directly combines heterogeneous sensor access with adaptive video configuration, while earlier sensor-network research considered semantic event-driven data collection [7], [8]. These works make a broad claim that sensor cues plus adaptive video analytics are unprecedented indefensible.

Video anomaly research provides evaluation and benchmark context [9], [10], [17]. Industrial visual anomaly benchmarks such as MVTec AD, MVTec LOCO AD, and Real-IAD are image-based; they support industrial inspection context but cannot validate temporal sampling or detection latency [13], [14], [16]. IPAD is directly relevant to industrial video, and recent work continues to evaluate industrial video anomaly methods on it [11], [12]. A rights-listed CC BY 4.0 conveyor dataset offers a narrower lab-scale foreign-object setting but only partial labels [18]. The project's dataset validation record therefore separates topical suitability from license clearance, temporal metadata, and annotation reliability.

The bounded question for SAGE is whether four policies produce different recall/latency/workload trade-offs when compared at identical frame quotas, and how controlled cue misses, false triggers, and delay affect those results. This pilot implements and exercises that comparison on three selected weakly labeled clips; it does not establish a new sampling algorithm or a general anomaly detector. The literature matrix is a focused map, not a systematic review. Elsevier's October 2026 source list verifies venue/source coverage for the cited publication years; the exact article DOI records were not individually verified in Scopus.

## IV. System and Experimental Method

### A. Data and ground truth

The broad-topic candidate IPAD was not used because dataset-specific reuse rights, timing, and annotation reliability remain unverified. Instead, the pilot uses the CC BY 4.0 Mendeley dataset *Image Dataset for Foreign Object Detection in Iron Ore Conveyor Belt Systems* (DOI 10.17632/s25x2bnshz.1) [18]. Three clips were evaluated: `boardcamera_iron_ore_7_wood_2`, `boardcamera_iron_ore_7_wood_3`, and `boardcamera_iron_ore_things`. The source videos contain 4,313, 3,907, and 4,982 decodable frames at 119.1829, 117.8108, and 119.3415 FPS, respectively, all at 1280 × 720. Five or six numbered extracted images per clip were matched to the same-index decoded source frames. A further spot check found byte-identical normal manual-split/source JPEGs for all three clips; three anomaly `_detected_1` files retained the matching source-video stem and counter and visually corresponded to the same-index source frames. Derived sequences contain 205, 167, and 169 JPEGs; unlabeled frames were omitted rather than interpolated. Labels come from manual-split folder membership and are weak frame annotations without documented inter-annotator reliability. Each selected anomaly run is represented as one event interval only for this bounded pilot. Dataset validation and the selected-frame checksum receipt are recorded in `docs/research/DATASET_VALIDATION.md` and `docs/research/evidence/manual_split_provenance_check.json`.

Each clip is represented by an identifier and event intervals containing [start, end, event type, ROI]. The evaluator reads the labels, and the present cue simulator reads event starts to create simulated cues; the detector does not read labels and schedulers only receive the generated cue stream. This indirect label-to-cue path makes sensor-guided conditions oracle-derived and can overstate realistic cue value. Report these as controlled simulations. A separate observable proxy or independently collected sensor stream is required before claiming independent multimodal evidence. Any calibration/evaluation split is performed by clip or device/process rather than adjacent frames. Dataset permissions, exclusions, transformations, privacy constraints, and annotation provenance will be reported.

### B. Perception methods

The implemented classical-CV baseline uses OpenCV MOG2 background subtraction on 320 × 240 grayscale scout frames (`history=120`, `varThreshold=32`, shadows disabled, learning rate 0.1 during the first four frames and 0.01 thereafter). The foreground-pixel fraction is the activity score; the configurable default threshold is 0.015. This detects visual change, not semantic abnormality or causality. The present baseline has no ROI-specific scoring or calibration/held-out threshold workflow; those settings must be frozen and reported for a dataset evaluation.

The OpenCV HOG descriptor uses pretrained linear-SVM pedestrian weights (`cv2.HOGDescriptor_getDefaultPeopleDetector()`). Frames are resized to 640 pixels wide and evaluated with 8 × 8 stride/padding and scale 1.05. It detects pedestrians only, so its conveyor run is a semantic-mismatch diagnostic, not an anomaly comparison.

For the binary anomaly comparison, the [ONNX Model Zoo ResNet-18 v1-7](https://huggingface.co/onnxmodelzoo/resnet18-v1-7) ImageNet weights (Apache-2.0 model card) produce 1,000 frozen logits from each 224 × 224 center-cropped, normalized RGB frame. A class-balanced logistic linear head is fit on weak/manual folder labels from two clips; the third whole source video is held out. Three folds yield 336, 374, and 372 training frames. The probability threshold is fixed at 0.5 and is not tuned on held-out clips. This is frozen-feature transfer learning, not full-network fine-tuning. It is aligned with the dataset's binary normal/anomaly labels, but limited by three selected videos, weak labels, one event per clip, and no independent annotation adjudication. Training code and model provenance are in `scripts/train_resnet18_probe.py` and `models/pretrained/README.md`.

### C. Simulated sensor cues

The current simulator samples each annotated event start with a configured detection probability, adds false triggers using a seeded per-second Bernoulli process, and applies a configured delay. Each policy in a paired comparison receives the same cue realization. Because event labels seed cues, sensor-guided results are oracle-derived simulations, not independent sensor evidence. These cues test sensitivity to controlled error and do not estimate physical sensor accuracy, placement, or communication behavior.

### D. Scheduling policies

1. **Fixed-rate:** uniformly spread a target quota across the clip, independent of visual activity and cues.
2. **Video-activity-adaptive:** prioritize frames whose current lightweight motion-scout score exceeds a threshold, with a deterministic fallback cadence to fill the shared quota.
3. **Sensor-triggered:** prioritize frames in an already-active simulated-cue window, with a deterministic fallback cadence to fill the shared quota.
4. **Budget-aware adaptive:** prioritize a frame when current visual activity or an already-arrived cue is present, with deterministic fallback under the same quota.

All policies share decoding, preprocessing, detector parameters, and evaluation clips. Each policy analyzes an exact common quota of `ceil(frame_count × budget_fraction)` frames; the quota is repeated at each predeclared budget fraction. The video-activity and budget-aware policies also scan each frame with the lightweight scout. Its measured time is charged to those policies; `processing_time_seconds` excludes media decoding, scheduler overhead, and output writing. Policy-specific parameters and per-frame decision traces are retained. The current CLI uses full-frame motion scores and does not yet configure per-clip regions of interest.

### E. Metrics

- Event recall is detected annotated events divided by all annotated events, with the matching rule and counts stated.
- Current `false_alarms` counts each detector-positive analyzed frame outside annotated intervals; it does not merge consecutive positive frames into alarm episodes. Report the frame-level counting rule and per clip-minute only where duration is valid.
- Latency is first valid detection time minus event start. Misses are reported separately; where original timestamps are unavailable, latency is in frames.
- Processing cost includes analyzed frame count/fraction and measured software runtime on a named machine. Modeled budget limits are identified separately.
- Trade-off plots show recall and latency against analyzed frames and measured runtime.

### F. Experimental matrix and analysis

| Factor | Planned comparison levels | Control/reporting rule |
|---|---|---|
| Policy | Four policies | Same clips and detector; matched budgets |
| Frame budget | 0.10, 0.25, 0.50 proposed | Each policy analyzes exactly `ceil(total frames × fraction)` frames |
| Cue detection | 1.0, 0.9, 0.5 proposed | Exact probabilities and seeds logged; simulator is oracle-derived from event starts |
| False triggers | 0 and 2 per minute proposed | Rate denominator and generated cue stream logged |
| Delay | 0 and 1 second proposed | Use source timing only after validating FPS/timestamps; otherwise define delay in frames |
| Clip condition | [quiet, intermittent, short/long events] | Per-clip outcomes shown |
| Detector | Classical CV and pretrained model | Model provenance and event compatibility reported |

Primary comparisons are paired by clip, budget, cue realization, and repetition seed. Report per-clip data and aggregate median with spread. If supported by the sample design, calculate paired bootstrap intervals at the clip level. No condition or metric will be omitted solely because it is unfavorable. A predeclared analysis plan and all parameter values will accompany final results.

## V. Implementation and Reproducibility

The implementation comprises `sage/engine.py`, `sage/cli.py`, `app.py`, and automated tests. The CLI writes CSV/JSONL policy metrics, per-event outcomes, and per-frame traces. The Streamlit dashboard inspects saved runs. The pilot used Python 3.12.10, OpenCV 4.14.0, NumPy 2.5.4, and Windows 10; a more detailed processor model was not available from the host inventory. Each budget/policy run processed the same derived sequence and seed 17. Detector runtime includes the scout pass for video-adaptive and budget-aware policies, but excludes media loading/decoding, scheduling overhead, and output writing. Host runtime is not edge latency or energy.

## VI. Results

### A. Dataset and run coverage

The public-data evaluation contains three clips and one weakly labeled anomaly run per clip. All four policies ran at 10%, 25%, and 50% of each clip, with total quotas of 55, 137, and 272 selected frames across the three clips. The same seed (17) was used throughout. A five-condition cue ablation ran at 25% for each clip. Results are descriptive only; there are no repeat seeds or independently adjudicated labels for inferential analysis.

### B. Primary policy comparison

| Budget | Policy | Event recall | False-positive frames | Latency (s) | Frames analyzed | Detector runtime (s) |
|---:|---|---:|---:|---:|---:|---:|
| 0.10 | Fixed-rate | 3/3 | 28 | varies by clip | 55 | 0.278 |
| 0.10 | Video-adaptive | 0/3 | 46 | missed | 55 | 3.070 |
| 0.10 | Sensor-triggered* | 3/3 | 24 | 0.000–0.0084 | 55 | 0.263 |
| 0.10 | Budget-aware* | 0/3 | 46 | missed | 55 | 3.076 |
| 0.25 | Fixed-rate | 3/3 | 73 | 0.000–0.0252 | 137 | 0.736 |
| 0.25 | Video-adaptive | 0/3 | 128 | missed | 137 | 3.507 |
| 0.25 | Sensor-triggered* | 3/3 | 59 | 0.000–0.0084 | 137 | 0.693 |
| 0.25 | Budget-aware* | 0/3 | 128 | missed | 137 | 3.499 |
| 0.50 | Fixed-rate | 3/3 | 144 | ~0.000–0.0084 | 272 | 1.430 |
| 0.50 | Video-adaptive | 1/3 | 221 | missed for 2 clips | 272 | 4.153 |
| 0.50 | Sensor-triggered* | 3/3 | 116 | 0.000–0.0084 | 272 | 1.427 |
| 0.50 | Budget-aware* | 1/3 | 221 | missed for 2 clips | 272 | 4.154 |

`*` Simulated cues are generated from the same event annotation used for evaluation. Sensor-assisted rows are oracle-derived and do not measure an independent sensor.

Across these selected clips and parameters, video-adaptive policies missed all three events at 10% and 25%, and detected one at 50%. Fixed-rate detected all three at every budget. The sensor-triggered policy also detected all three, but cues are annotation-derived and fallbacks can sample events without cues. The near-zero cue-assisted latency follows from event-start-driven simulation and must not be interpreted as observed sensor latency. False-positive frames and runtimes sum across three clips; runtime excludes decoding, scheduler overhead, and writing. There are too few independently validated events and no repeated seeds to support a stable policy ranking.

### C. Cue-quality ablation

At the 25% budget, five cue conditions were run for four policies on each of three clips (60 policy-condition rows). The cue conditions vary detection probability, false triggers, delay, and absence of cues. This controlled simulation is not an estimate of real sensor performance; event starts seed cue generation, and fallback sampling may detect events without cues. The per-clip ablation CSVs, event rows, and traces are preserved under `results/mendeley_conveyor_{pilot,wood3,things}_ablation/`; see the pilot record for interpretation boundaries.

### D. Classical CV and pretrained model comparison

The classical MOG2 activity detector was evaluated against three weakly labeled conveyor runs. OpenCV's pretrained HOG pedestrian detector ran at a 25% budget on the first clip and returned zero positive frames. HOG detects pedestrian presence, while this dataset labels foreign-object anomalies. Its zero recall and false-positive count are a semantic-mismatch diagnostic, not a comparative anomaly-detection result. The dataset's separate YOLOv8 weights detect the belt center region, and the `conveyor` box labels do not mark foreign objects; those weights are not used as anomaly detections.

#### Clip-held-out ResNet probe

Each selected clip was evaluated using a logistic head trained on the other two source videos. All policies used the same exact per-clip quotas as the MOG2 runs; aggregate quotas were 55, 137, and 272 frames at 10%, 25%, and 50%. The fixed 0.5 probability threshold was set before held-out evaluation.

| Budget | Policy | Event recall | False-positive frames | Frames analyzed | Summed host detector runtime (s) |
|---:|---|---:|---:|---:|---:|
| 0.10 | Fixed-rate | 3/3 | 13 | 55 | 1.220 |
| 0.10 | Video-adaptive | 0/3 | 13 | 55 | 3.735 |
| 0.10 | Sensor-triggered* | 3/3 | 7 | 55 | 1.198 |
| 0.10 | Budget-aware* | 0/3 | 13 | 55 | 3.755 |
| 0.25 | Fixed-rate | 3/3 | 25 | 137 | 2.891 |
| 0.25 | Video-adaptive | 0/3 | 38 | 137 | 5.393 |
| 0.25 | Sensor-triggered* | 3/3 | 22 | 137 | 2.822 |
| 0.25 | Budget-aware* | 0/3 | 38 | 137 | 5.347 |
| 0.50 | Fixed-rate | 3/3 | 51 | 272 | 5.681 |
| 0.50 | Video-adaptive | 1/3 | 75 | 272 | 8.129 |
| 0.50 | Sensor-triggered* | 3/3 | 45 | 272 | 5.529 |
| 0.50 | Budget-aware* | 1/3 | 75 | 272 | 7.937 |

At 25%, event recall matches the MOG2 table, while the ResNet probe generates fewer false-positive frames and takes more measured detector time. These are descriptive results from one seed, three held-out clips, and weak/manual interval labels. The sensor-triggered rows remain oracle-derived. ONNX session initialization, decoding, scheduler overhead, and output writing are excluded from processing time.

## VII. Discussion

The pilot shows that an activity threshold can prioritize normal conveyor motion and miss labeled anomaly runs at a fixed quota. Uniform sampling detected all three selected events at each tested budget with both MOG2 and the clip-held-out ResNet probe. At 25%, the ResNet probe produced fewer false-positive frames at a higher host runtime. This small pattern suggests a compute/false-positive trade-off to test, not a general model or policy ranking. Cue-assisted runs cannot establish value because the simulator receives annotation-derived event starts; fixed-rate and no-cue fallback can also detect events. Follow-up work should add independently adjudicated events, more source-video groups, repeated seeds, independent cue observations, and calibration/uncertainty analysis.

## VIII. Limitations, Ethics, and Future Work

Simulation does not validate physical sensor detection, false-trigger rates, timing, placement, communication, or integration. The current simulator derives cues from event starts and therefore gives sensor policies oracle-derived information. Host runtime is not an edge-device or energy measurement. Motion detectors are sensitive to camera movement, lighting, shadows, and occlusion; pretrained HOG detects pedestrians only and is not comparable to general machine-anomaly labels. Current false alarms are frame counts, not alarm episodes, and precision/F1 are not presently reported. Dataset temporal representation and annotation quality constrain latency and event claims. A small selected clip set supports conclusions only for the tested conditions. The literature map is not a systematic review.

The dataset record displays CC BY 4.0; retain attribution and inspect for third-party content. Dataset-wide label quality has not been independently verified. The derived pilot has three selected weakly labeled events and one seed. The ResNet probe trains on two clips and tests on one per fold, but its weak labels, small number of held-out source videos, ImageNet domain shift, and uncalibrated 0.5 threshold limit the comparison. MOG2 is sensitive to motion, lighting, camera movement, shadows, and occlusion. False positives are frame counts rather than alarm episodes. HOG semantics do not match foreign-object labels. Simulated cues, modeled quotas, and current-host runtime do not validate physical sensors, edge-device latency, energy, or field reliability.

## IX. Conclusion

SAGE produced matched-budget traces for four policies on three selected weakly labeled clips. The clip-held-out ResNet-18 linear probe matched MOG2 event recall and yielded fewer false-positive frames at 25%, with higher host processing time. This is a narrow exploratory transfer-learning result, not a validated industrial anomaly detector. Annotation-derived cues remain oracle-assisted, labels are not independently validated, and these three clips cannot establish broad industrial performance, physical sensor benefit, edge savings, or energy savings.

## References

The focused bibliography with relevance notes and Scopus caveat is in `docs/research/LITERATURE_MATRIX.md`.

[1] R. Xu, S. Razavi, and R. Zheng, “Edge Video Analytics: A Survey on Applications, Systems and Enabling Techniques,” *IEEE Communications Surveys & Tutorials*, 25(4), 2951–2982, 2023, doi: 10.1109/COMST.2023.3323091.

[2] S. Zhang, C. Wang, Y. Jin, J. Wu, Z. Qian, M. Xiao, and S. Lu, “Adaptive Configuration Selection and Bandwidth Allocation for Edge-Based Video Analytics,” *IEEE/ACM Transactions on Networking*, 30(1), 285–298, 2022, doi: 10.1109/TNET.2021.3106937.

[3] B. Qian, Z. Wen, J. Tang, Y. Yuan, A. Y. Zomaya, and R. Ranjan, “OsmoticGate: Adaptive Edge-Based Real-Time Video Analytics for the Internet of Things,” *IEEE Transactions on Computers*, 72(4), 1178–1193, 2023, doi: 10.1109/TC.2022.3193630.

[4] J. Lin, P. Yang, W. Wu, N. Zhang, T. Han, and L. Yu, “Learning-Based Query Scheduling and Resource Allocation for Low-Latency Mobile-Edge Video Analytics,” *IEEE Internet of Things Journal*, 11(3), 4872–4887, 2024, doi: 10.1109/JIOT.2023.3300696.

[5] C. Wang, P. Yang, J. Hou, Z. Liu, and N. Zhang, “Dependence-Aware Multitask Scheduling for Edge Video Analytics With Accuracy Guarantee,” *IEEE Internet of Things Journal*, 11(16), 26970–26983, 2024, doi: 10.1109/JIOT.2024.3397296.

[6] Y. Li, A. Padmanabhan, P. Zhao, Y. Wang, G. H. Xu, and R. Netravali, “Reducto: On-Camera Filtering for Resource-Efficient Real-Time Video Analytics,” in *Proceedings of ACM SIGCOMM*, 359–376, 2020, doi: 10.1145/3387514.3405874.

[7] D. Zhong, M. Zhu, and B. Huang, “MACEdge: Real-Time Video Analytics Based on Multi-Access Collaborative Edge Computing,” in *Proceedings of the IEEE International Conference on Systems, Man, and Cybernetics*, 3639–3645, 2023, doi: 10.1109/SMC53992.2023.10393957.

[8] R. Vaisenberg, S. Mehrotra, and D. Ramanan, “Exploiting Semantics for Scheduling Real-Time Data Collection from Sensors to Maximize Event Detection,” *SPIE Multimedia Computing and Networking*, vol. 7253, 2009, doi: 10.1117/12.816255.

[9] B. Ramachandra, M. J. Jones, and R. R. Vatsavai, “A Survey of Single-Scene Video Anomaly Detection,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 44(5), 2293–2312, 2022, doi: 10.1109/TPAMI.2020.3040591.

[10] A. Acsintoae et al., “UBnormal: New Benchmark for Supervised Open-Set Video Anomaly Detection,” in *Proceedings of CVPR*, 2022, doi: 10.1109/CVPR52688.2022.01951.

[11] J. Liu et al., “IPAD: Industrial Process Anomaly Detection Dataset,” *IEEE Transactions on Circuits and Systems for Video Technology*, 35(1), 380–393, 2025, doi: 10.1109/TCSVT.2024.3465517.

[12] Q. Yu, K. Zhu, Y. Cao, and Y. Kang, “INFP: INdustrial Video Anomaly Detection via Frequency Prioritization,” in *Proceedings of IJCAI*, 2296–2304, 2025, doi: 10.24963/ijcai.2025/256.

[13] P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger, “MVTec AD—A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection,” in *Proceedings of CVPR*, 2019, doi: 10.1109/CVPR.2019.00982.

[14] P. Bergmann, K. Batzner, M. Fauser, D. Sattlegger, and C. Steger, “Beyond Dents and Scratches: Logical Constraints in Unsupervised Anomaly Detection and Localization,” *International Journal of Computer Vision*, 2022, doi: 10.1007/s11263-022-01578-9.

[15] “Anomaly Detection in Industrial Machinery Using IoT Devices and Machine Learning: A Systematic Mapping,” *IEEE Access*, 11, 128288–128305, 2023, doi: 10.1109/ACCESS.2023.3333242.

[16] C. Wang et al., “Real-IAD: A Real-World Multi-View Dataset for Benchmarking Versatile Industrial Anomaly Detection,” in *Proceedings of CVPR*, 2024, doi: 10.1109/CVPR52733.2024.02159.

[17] B. Ramachandra and M. Jones, “Street Scene: A New Dataset and Evaluation Protocol for Video Anomaly Detection,” in *Proceedings of WACV*, 2020, doi: 10.1109/WACV45572.2020.9093457.

[18] F. L. M. de Sousa, T. E. A. de Oliveira, B. N. Coelho, and S. E. D. Silva, “Image dataset for foreign object detection in iron ore conveyor belt systems,” *Data in Brief*, vol. 60, 111537, 2025, doi: 10.1016/j.dib.2025.111537; dataset doi: 10.17632/s25x2bnshz.1.

[19] C.-C. Hung et al., “VideoEdge: Processing Camera Streams using Hierarchical Clusters,” in *Proceedings of the IEEE/ACM Symposium on Edge Computing*, 2018, doi: 10.1109/SEC.2018.00016.

[20] Z. Xiao, Z. Xia, H. Zheng, B. Y. Zhao, and J. Jiang, “Towards Performance Clarity of Edge Video Analytics,” in *Proceedings of the ACM/IEEE Symposium on Edge Computing*, 2021, doi: 10.1145/3453142.3491272.

Elsevier's official October 2026 source list shows that all cited venues/sources were covered by Scopus for their publication years. This source/year verification does not prove that the exact DOI/article records are indexed; those records were not individually checked in Scopus. See `docs/research/SCOPUS_SOURCE_AUDIT.md`.
