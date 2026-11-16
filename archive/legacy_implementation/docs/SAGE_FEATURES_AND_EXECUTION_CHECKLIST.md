# SAGE Feature Inventory, Chat Plan, and Execution Checklist

**Reconciled:** 2026-11-02  
**Scope authority:** `00_Master/SAGE_Technical_Project_Report.md` and its DOCX, v1.2  
**Implementation owner:** Claude Code  
**ChatGPT role:** feature planning, Claude prompt generation, and debugging/review of Claude's reports  
**Status:** Software demo works on synthetic footage. Real-data evaluation, dataset validation, and the required detector-by-policy study remain open.

This checklist is the working execution plan. It does not change the research scope or claim that an unchecked item is complete. When code, data, or project decisions change, update this file and the project change log through the feature-specific Claude Code task.

## 1. Decisions to preserve

- SAGE is a simulation-first industrial video-monitoring research project for production-line/conveyor scenarios.
- The current-semester study uses real public industrial video and simulated sensor cues. Physical sensors and edge hardware are future work.
- The four scheduling policies are fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware adaptive.
- **Classical CV versus a pretrained model is required.** The user has decided the policy study must run under **both detector types across all four policies**: a 2 × 4 detector/policy matrix, with equal clips, annotations, ROI, timing, metric rules, cue realization, and matched frame quota within each paired run.
- The project targets multiple event types. The final categories and event definitions depend on what the validated data can support. Do not silently reduce the task to one event type; if the data cannot support multiple types, bring the evidence and proposed scope decision back to the user.
- IPAD is a leading candidate, not a selected/validated dataset. The iron-ore conveyor dataset is an alternative. Dataset, event taxonomy, ROI, exact pretrained model, and protocol values remain open until validation.
- The pretrained model must be selected for the validated event labels. OpenCV HOG+SVM currently detects people only; it is a software comparator candidate, not a general industrial-anomaly model.
- Do not claim measured physical sensor behavior, Raspberry Pi performance, energy savings, real-time performance, safety effectiveness, deployment readiness, or unsupported novelty.
- Do not fabricate results. Keep synthetic demo output visibly separate from real-data results.

## 2. Current project snapshot

| Area | Current evidence | Status |
|---|---|---|
| Master scope | Technical Project Report v1.2 is active. The MD and DOCX were reported as matching; the PDF remains v1.0 per the cleanup log. | Use v1.2 MD/DOCX as authority; PDF re-export and visual verification remain open. |
| Project organization | `00_Master`, `03_Assets`, `04_Implementation`, `05_Archive`, and `06_Admin` exist. Claude has already reorganized and documented the folder. | Preserve the existing structure. |
| Implementation | `04_Implementation` contains the Python package, CLI, Streamlit app, tests, docs, and generated demo outputs. | Runnable software baseline. |
| Synthetic demo | 70 generated frames; 4 policies; 18 selected frames per policy at the default 25% quota; 8 event rows; 280 frame-trace rows. | Verified synthetic smoke only; not industrial evidence. |
| Tests | Claude reports 8/8 `unittest` checks passing after adding `data_source` to event-level outputs. | Re-run after each relevant code change; keep test logs in feature chat. |
| Dashboard | Demo summary and event rows load; synthetic warnings appear; missing-file issue is resolved. | Remaining: prominently label synthetic KPI/chart values, not only warning banners. |
| Dataset archive | `P:\Dev\Projects\SAGE\IPAD_dataset.zip` is present, 8,920,232,221 bytes at the latest inspection. | Downloaded, but integrity, contents, license, timing, annotations, and suitability are not yet verified. No extracted data folder appeared in the latest inventory. |
| Dataset selection | IPAD is a candidate; the report also lists the 2025 iron-ore conveyor dataset as an alternative. | Open pending the validation gate. |
| Pretrained model | `hog_people` exists in code and loads, but only detects people/workers. | Do not call this the final model unless selected events and annotations support person detection. |
| Version control | Local Git repository initialized at `P:\Dev\Projects\SAGE` (2026-11-02), branch `master`; root `.gitignore` verified to exclude the archive, `.venv`, raw data, generated outputs/results, caches, partial downloads, and weights. 38 source/doc files are prospective baseline candidates; nothing staged, no commits, no remotes. | Initialization done; the initial baseline commit has not been made and awaits user approval. Review the staged set before committing. |
| Documentation consistency | The implementation README says IPAD is selected/not downloaded and that four reference documents are unchanged. The v1.2 report says dataset selection is open; the archive is now present; the master report has been updated. | Reconcile implementation docs against the current report and file state. Do not alter the master report unless the user approves a scope/decision change. |

## 3. Feature inventory and acceptance checklist

### A. Project control, safe files, and version history

- [ ] Confirm the v1.2 MD/DOCX are the active canonical report and record the PDF's v1.0 status.
- [ ] Reconcile `04_Implementation/README.md`, `docs/SAGE_SPECIFICATION.md`, `docs/DATASET_AND_PROVENANCE.md`, `docs/USAGE.md`, and the manuscript draft with the v1.2 report and current downloaded archive.
- [x] Establish a root-level `.gitignore` before any Git add. Exclude `.venv/`, `IPAD_dataset.zip`, `*.crdownload`, extracted raw data, generated `results/` and `outputs/`, caches, and any large external weights. *(2026-11-02: root `.gitignore` added; `git check-ignore -v --no-index` confirms the archive, `.venv/`, `IPAD_dataset/` and both `data/` paths, root and `04_Implementation` `results/`/`outputs/` including synthetic demo output, caches, `*.crdownload`, and weight/checkpoint patterns; `04_Implementation/.gitignore` unchanged.)*
- [x] Initialize/verify version control and record the clean starting state. Review all staged files before any commit; never stage the dataset or virtual environment. *(2026-11-02: `git init` at `P:\Dev\Projects\SAGE`, branch `master`, no remotes, 0 tracked/staged files, no commits. `git add --dry-run --all` previews 38 source/doc files (~2.0 MB); ignored: `.venv/`, `04_Implementation/results/`, `IPAD_dataset.zip`. Initial baseline commit awaits user approval.)*
- [ ] Update `06_Admin/SAGE_Change_Log.md` and the file audit to record the implementation, current archive state, and any new approved decision.
- [ ] Preserve the current folder structure, archived originals, current master report, and existing user files.

**Acceptance:** a clean status shows only intended source/docs changes; large data, `.venv`, generated outputs, and archives are excluded; a reviewer can identify the authoritative report and current implementation.

### B. Dataset archive validation and selection (critical gate)

- [ ] Verify the archive's exact path, byte size, SHA-256, and archive integrity using a suitable read-only listing/test before extraction.
- [ ] Confirm the actual download source matches an official/author-approved source; record retrieval date and source URL.
- [ ] Verify dataset-specific terms for academic analysis, local storage, derived outputs, figures/demo display, and redistribution/publication. Website or paper licensing must not be assumed to license video data.
- [ ] Inspect archive layout, compressed/uncompressed sizes, file types, device/clip folders, splits, annotations, and documentation without changing the archive.
- [ ] Validate sequence boundaries, natural frame order, gaps/resets/duplicates, timestamps/FPS, cycle-period metadata, and label alignment. Do not infer source timing from filenames alone.
- [ ] Compare IPAD with the report's iron-ore conveyor alternative against the same criteria: rights, continuous video, usable timing, multiple event types, labels, and detector compatibility.
- [ ] Select and record one dataset only after the gate passes. Record excluded candidates and why.
- [ ] Extract verified data to an ignored `04_Implementation/data/raw/...` path; keep the original archive intact until extraction and checksums are verified.
- [ ] Create a provenance manifest with source/version, retrieval date, license evidence, archive hash, clip/device IDs, splits, frame rate/timing, annotations, transformations, and exclusions.

**Gate:** no dataset-specific model decision, latency claim, annotation-derived result, or real-data manuscript finding until integrity, rights, ordering/timing, labels, and dataset choice are documented.

### C. Event taxonomy, annotations, ROI, and evaluation rules

- [ ] Define multiple data-supported industrial event types from the v1.2 candidate list and validated footage; record why each type is observable and measurable.
- [ ] Define start/end convention, event overlap rules, event identity, event-to-detection matching window, false-alarm treatment, and how repeated detections are grouped.
- [ ] Map source annotations to SAGE event intervals without using test labels in policy or detector decisions.
- [ ] Define a fixed ROI (or documented ROI set) for each relevant camera/clip; make ROI coordinates reproducible and use the same ROI for both detectors and all policies.
- [ ] Define calibration/evaluation separation by clip/device/process, not by adjacent frames. Freeze event rules, thresholds, and ROI before final evaluation.
- [ ] Add an annotation validator/converter for the chosen dataset's native format and test it against manually inspected sample events.

**Acceptance:** each evaluated event row has a clip, event type, interval, ROI where used, provenance, and a deterministic matching result; scheduler inputs cannot access ground-truth labels.

### D. Classical CV and pretrained detector comparison

- [ ] Keep an interpretable classical baseline. Current MOG2 motion scoring is a starting implementation; validate it on real clips and ROI.
- [ ] Implement/evaluate frame differencing alongside background subtraction as directed by the report where feasible; compare activity quality and processing cost without tuning on held-out data.
- [ ] Select at least one pretrained model after dataset/event validation. It must detect the same event types used in the comparison, have documented class coverage, weights source/license, version, input resolution, thresholds, and runtime.
- [ ] Treat `hog_people` as a person/worker-only candidate. Replace or supplement it if the selected industrial event types are conveyor/material anomalies rather than people.
- [ ] Use identical validated footage, event definitions, ROI, annotations, matching rules, and calibration policy for classical and pretrained detectors.
- [ ] Run the user-approved **both detectors × all four scheduling policies** matrix, separately reporting detector comparison and sampling-policy effects. Hold the detector fixed within every four-policy comparison.
- [ ] Record inference time/processed frame and resource measures that can be reliably measured on the named host. Do not call these edge-device/energy measurements.

**Acceptance:** all 8 detector-policy combinations run on semantically compatible labels; results identify detector/model versions and never compare mismatched event meanings.

### E. Sensor-cue simulator and robustness conditions

- [x] Seeded cue simulator with event detection probability (misses), false-trigger rate, delay, and paired cue realization is implemented.
- [ ] Define the cue-generation rule from physically observable events; pass the anti-oracle review in Report v1.2 before final runs.
- [ ] Decide and document timing jitter, sensor sampling frequency, cue persistence/debounce, placement/field-of-view assumptions, and how each is represented or explicitly omitted.
- [ ] Predeclare nominal, missed-trigger, false-trigger, delayed, and noisy/jittered conditions with parameter values and seeds. Keep values labeled simulated, not measured.
- [ ] Verify that the same generated cue stream is used across each paired policy comparison and that cues cannot trigger before their plausible observation time.
- [ ] Add tests for determinism, delay/miss/noise boundaries, and absence of future-label look-ahead.

### F. Scheduling policies and matched-budget controls

- [x] Four policies exist: fixed-rate, video-activity-adaptive, sensor-triggered, and budget-aware adaptive.
- [x] Current engine enforces one exact target frame quota across policies and writes per-frame traces on synthetic runs.
- [ ] Reconcile each implemented policy rule and its causal/online assumptions with Report v1.2; document any full-frame activity-scout cost.
- [ ] Verify that fixed-rate is the uniform baseline; video-only uses current visual activity; sensor-triggered uses only arrived cues; budget-aware combines available signals while enforcing the budget.
- [ ] Predeclare low/medium/high matched frame budgets and any minimum revisit/latency safeguards. Report actual selected counts, not only target percentages.
- [ ] Ensure all 4 policies share the same input, detector, ROI, preprocessing, event rules, condition, cue stream, software/hardware environment, and evaluation split.
- [ ] Measure/estimate scheduling overhead separately from image-processing cost, as required by Report v1.2 §4.2; label modeled values and measured host runtime separately.
- [ ] Add edge-case tests: short clips, 100%/small budgets, no cues, continuous activity, cue at boundaries, overlapping events, and deterministic repeats.

### G. Benchmark runner, metrics, and analysis

- [x] CSV/JSONL summary, event-level rows, per-frame traces, sensor settings, seed, source label, and model/library versions are represented in the software baseline.
- [ ] Build the complete real-data run matrix: **2 detectors × 4 policies × each matched budget × each cue-quality condition × each selected clip/event type × predeclared repetitions/seeds**.
- [ ] Implement/check all report metrics: event precision/recall, false alarms (count and per clip-minute), event latency distribution, misses/missed-event rate, frames processed/fraction, processing time, throughput where meaningful, and scheduling overhead separately.
- [ ] Verify metric calculations against hand-computed fixtures and event-level denominators; report per-clip and per-event-type results as well as aggregate summaries.
- [ ] Record host/software versions, warm-up, repetitions, seeds, configs, input IDs, FPS/timing basis, detector version, and failures.
- [ ] Use paired analysis by clip/condition; calculate uncertainty (e.g., clip-level paired bootstrap) only if the sample design supports it. Preserve negative and unfavorable findings.
- [ ] Keep synthetic demo outputs under an unmistakable synthetic source label; never include them in real-data aggregates.
- [ ] Generate an immutable run manifest linking outputs to dataset release, code version/commit, config, seeds, and annotation version.

### H. Streamlit dashboard

- [x] Dashboard loads saved summary and event-level CSVs, filters/exports them, and warns for synthetic data.
- [ ] Label synthetic values directly in KPI titles/charts/tables (not only a warning banner) so screenshots cannot be misread when separated from context.
- [ ] Add views/filters for dataset/clip, event type, ROI where relevant, detector/model, all four policies, matched budget, cue condition, seed/run, and synthetic-vs-real source.
- [ ] Show the 2 × 4 comparison without pooling incompatible event labels; show misses and latency distributions, not just means.
- [ ] Show per-clip/event rows and traces; expose the run manifest/settings and enable filtered summary and event-level export.
- [ ] Smoke-test the dashboard from the documented working directory with synthetic data and then validated real data; check startup, missing-file behavior, and exports.

### I. Software quality, environment, and documentation

- [x] Python package/CLI, local requirements, synthetic smoke workflow, and 8 reported unit tests exist.
- [ ] Retain and expand `unittest` coverage; pytest is optional, not a requirement.
- [ ] Add tests for the real dataset adapter, annotation conversion, ROI, both detectors, full 2 × 4 matrix, ablation rows, provenance, and dashboard synthetic/real distinction.
- [ ] Ensure a clean environment can install from `requirements.txt` and run CLI/demo/dashboard exactly as documented; pin compatible OpenCV below 5 while HOG API is used.
- [ ] Reconcile README and implementation docs with Report v1.2 and current archive status (IPAD candidate open, archive present but unvalidated; HOG is not the final model).
- [ ] Reconcile `06_Admin` audit/change log with the implementation, v1.2 report, downloaded archive, and current Git status.
- [ ] Verify the v1.2 DOCX/MD and re-exported PDF; preserve the v1.0 PDF as an archive until the new PDF is visually checked.

### J. IEEE-style manuscript and research record

- [x] A structured manuscript draft/protocol exists and contains no fabricated experiment findings.
- [ ] Verify the closest related work and dataset citations from primary sources; keep novelty claims narrow and evidence-based.
- [ ] Finalize methods only after dataset, event types, ROI, model, cue model, metrics, and matrix are frozen.
- [ ] Populate results from immutable real-data runs only: dataset/provenance, 2 × 4 results, budgets, cue ablations, event-wise errors, runtime/overhead, uncertainty, and limitations.
- [ ] Ensure abstract, tables, figures, discussion, and conclusion match the actual outputs; report negative/inconclusive results.
- [ ] Keep publication/redistribution rules distinct from permission to download or analyze the data.

### K. Next-semester extension (future work, not v1 completion)

- [x] A physical-extension plan exists; no physical sensor, microcontroller, Raspberry Pi, edge deployment, or energy measurement is claimed complete.
- [x] Deeper ML/DL anomaly detection is documented as future work.
- [ ] Next semester: choose hardware/interface after v1 evidence; characterize real sensor error/timing; run paired real-cue vs simulated-cue tests; measure edge compute/memory/thermal/energy with an explicit instrument; develop a deeper anomaly model only after data/model fit is established.

## 4. Ordered execution gates

1. **Control baseline:** protect files, reconcile v1.2 docs, establish Git/ignore rules, record starting state.
2. **Data gate:** validate the downloaded archive, rights, structure, timing, and annotations; choose IPAD or the conveyor alternative.
3. **Task gate:** select multiple supported event types, define ROI, interval rules, and train/calibration/test splits.
4. **Detector gate:** validate classical activity methods and select a compatible pretrained model; keep model comparison distinct from policy comparison.
5. **Protocol gate:** freeze sensor cue semantics/conditions, four causal policy definitions, matched budgets, metrics, repetitions, and 2 × 4 matrix.
6. **Runner gate:** execute small real-data pilot, inspect traces and event matches, fix issues, then freeze settings.
7. **Evaluation gate:** run complete paired matrix and ablations; retain failures and raw outputs; analyze per clip/type.
8. **Dashboard gate:** display the completed real-data results with clear source labels and exports.
9. **Manuscript gate:** write final evidence-based IEEE manuscript and figures from the immutable result manifest.
10. **Future-work gate:** keep hardware/deeper-ML design separate from v1 claims.

Do not cross a gate until its acceptance conditions are written down and met. If a gate fails, return to the feature chat that owns it and revise the Claude Code prompt; do not quietly skip the requirement.

## 5. ChatGPT chats to create

Keep one **SAGE Control & Decisions** chat (this planning thread can serve as it). Create one feature chat at a time; each chat should produce scoped requirements, one Claude Code task prompt, acceptance criteria, and a review/debug loop. Claude Code performs all implementation and command execution. Paste Claude's summary, relevant diff, and test output back into that feature's ChatGPT chat.

| Order | Suggested ChatGPT chat title | Scope and exit artifact |
|---:|---|---|
| 0 | **SAGE — Control, Scope & Decision Register** | Master plan; enforce Report v1.2 and the user's decision of both detectors × all four policies; record decisions and gate status. No code implementation. |
| 1 | **SAGE — Git Baseline & Safe Project Layout** | Root `.gitignore`, verify/init Git, protect `.venv`, the 8.9 GB archive, results, and partial downloads; document a safe baseline. Review staged files before committing. |
| 2 | **SAGE — Dataset Archive Validation & Selection** | Inspect `IPAD_dataset.zip` safely, verify source/license/hash/integrity/contents/timing/annotations, compare the conveyor alternative, and recommend dataset selection with evidence. |
| 3 | **SAGE — Event Taxonomy, Annotations & ROI** | Map multiple validated event types, intervals, ROI, label conversion, matching rules, splits, and annotation QA. |
| 4 | **SAGE — Classical CV & Activity Features** | Validate MOG2 and frame differencing on selected footage/ROI; freeze calibration parameters and failure cases. |
| 5 | **SAGE — Pretrained Model Selection & Detector Matrix** | Select a pretrained model for the actual labels; document weights/license/version; run both detectors across all four policies; retire HOG if it is semantically unsuitable. |
| 6 | **SAGE — Sensor-Cue Model & Robustness** | Specify anti-oracle cue source, delays, misses, false triggers, jitter/debounce and levels; design reproducible ablations. |
| 7 | **SAGE — Four Scheduling Policies & Equal Budgets** | Audit causal definitions, exact common quotas, policy overhead, traces, and matched low/medium/high frame budgets. |
| 8 | **SAGE — Benchmark Matrix, Metrics & Statistics** | Build the 2 × 4 × budgets × cue conditions × clips/types × seeds experiment plan; metrics, manifests, paired analysis, and uncertainty. |
| 9 | **SAGE — Dashboard & Result Interpretation** | Real/synthetic source labels, 2 × 4 display, event type filters, latency/misses, traces, and exports. |
| 10 | **SAGE — Verification & Reproducibility** | Clean environment, `unittest`, integration, data adapter, CLI, dashboard smoke, run manifest, version capture, and final acceptance audit. |
| 11 | **SAGE — IEEE Manuscript & Literature Evidence** | Verify related work and write methods/results/limitations from frozen runs; no unsupported claims. |
| 12 | **SAGE — Next-Semester Hardware & Deep ML Plan** | Future camera/sensors/edge device and deeper ML/DL only; preserve the boundary from v1 evidence. |

### Standard instructions to put at the top of every feature chat

> Use the v1.2 master report and `SAGE_FEATURES_AND_EXECUTION_CHECKLIST.md` as scope authority. This chat handles only the named feature: clarify requirements, generate a concrete Claude Code prompt, and debug Claude's returned output. Claude Code alone edits project files and runs implementation commands. Preserve existing documents/data, never invent results, and stop for user input if the feature conflicts with a frozen decision or a prior gate. End each task with changed files, commands/tests, evidence, limitations, and checklist updates.

## 6. Open decisions still requiring evidence or user review

- Dataset selection: IPAD versus the iron-ore conveyor dataset, after archive and rights validation.
- Exact pretrained model: must support the selected event labels; HOG is not a general anomaly model.
- Specific multiple event categories, ROI definitions, and source annotation mapping.
- Whether the IPAD source timing supports seconds-based latency or only frame/replay-time latency.
- Predeclared budgets, cue condition values, number/diversity of clips, repeats/seeds, and statistical analysis plan.
- Exact classical activity algorithms and final calibration parameters.
- Initial Git baseline commit (repository initialized and ignore rules verified; commit not yet approved or made) and data-retention choices.

The user has now resolved one previous open item: **run the four-policy study under both detector types**. All future experiment plans and Claude prompts must preserve that 2 × 4 requirement.
