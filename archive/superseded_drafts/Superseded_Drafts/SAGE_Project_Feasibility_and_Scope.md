---
deadline: 10 days from scope freeze
document_type: Project feasibility and scope specification
last_updated: 2026-10-28
project: SAGE
status: Proposed scope; implementation not started
title: SAGE --- Project Feasibility Review and Scope Decision
version: 1.0
---

# SAGE --- Project Feasibility Review and Scope Decision

> **Document purpose:** Establish the proposed research direction,
> feasibility boundaries, experimental requirements, and acceptance
> criteria for the SAGE project. This document is intended to serve as a
> shared reference for the project repository, ChatGPT Project, Codex
> workflow, and academic planning.
>
> **Decision status:** Ready to narrow and freeze the research
> direction; implementation has not started.

## Table of Contents

1.  [Executive summary](#executive-summary)
2.  [Feasibility assessment](#1-feasibility-assessment)
3.  [Research direction](#2-reconsidering-the-research-direction)
4.  [System behavior and architecture](#3-what-the-final-system-will-do)
5.  [DAA algorithms and
    evaluation](#4-how-we-will-make-the-daa-component-substantial)
6.  [Computer-vision
    pipeline](#5-making-the-computer-vision-component-legitimate)
7.  [Six-subject
    mapping](#6-how-the-six-subjects-map-to-this-revised-scope)
8.  [Scope boundaries](#7-what-is-inside-and-outside-the-10-day-scope)
9.  [Paper and publication
    strategy](#8-the-paper-and-publication-strategy)
10. [Final scope decision](#9-final-scope-decision)
11. [Decision register and
    assumptions](#decision-register-and-assumptions)
12. [Open questions](#open-questions)
13. [Acceptance criteria](#acceptance-criteria)
14. [Implementation checklist](#implementation-checklist)
15. [References](#references)

## Executive summary

SAGE is proposed to become a **sensor-guided adaptive video-sampling
system**. It will process real video with classical computer-vision
methods, generate reproducible simulated sensor events, and compare four
sampling/scheduling policies under controlled computational budgets.

The intended research focus is the trade-off between event-detection
quality and processing cost. The project must distinguish measured
results from simulation assumptions and must not claim physical sensor
integration, Raspberry Pi performance, or research novelty unless those
claims are directly supported by evidence.

**Recommended scope:** one integrated Python application, a reproducible
experiment runner, quantitative evaluation, an interactive dashboard,
software-engineering artifacts, and an IEEE-structured manuscript.

The new deadline changes my recommendation. With **10 days, real-video
computer vision, a dashboard, six subjects to satisfy, and an
IEEE-structured paper**, we should optimize for a working,
experimentally defensible research system rather than a physically
ambitious prototype.

I would retain the central idea of SAGE---intelligent allocation of
limited observation and computation---but reconsider whether physically
moving a camera between zones is the best way to express that idea in
software.

My principal concern is not whether you can write the code in 10 days.
It is whether the final project will have enough **substantive DAA
analysis, genuine DIP/CV work, rigorous experimental results, and
traceable engineering artifacts** to satisfy the six subjects
independently.

We should design around those requirements first.

## 1. Feasibility assessment

  -----------------------------------------------------------------------
  Requirement             Feasibility in 10 days  Decision
  ----------------------- ----------------------- -----------------------
  DAA: multiple           High                    Make scheduling
  algorithms, complexity                          optimization the
  analysis, benchmarking                          research core

  Sensors &               High for a simulated    Simulate sensor events
  Microcontrollers        model; actual hardware  and noise explicitly
                          evidence depends on the 
                          rubric                  

  DIP/CV: real video and  High                    Use OpenCV on real
  image-processing                                video
  operations                                      

  Software Engineering:   High, with controlled   Produce artifacts
  GitHub, requirements,   documentation scope     alongside development
  UML, testing                                    

  Embedded Systems        Moderate if limited to  Model processing
                          edge-resource           budgets and latency;
                          simulation              avoid claiming
                                                  unmeasured hardware
                                                  performance

  PBL: integrated         High                    Build one integrated
  prototype and research                          system, not separate
  report                                          subject demonstrations

  Interactive dashboard   High with a lightweight Use Streamlit or an
                          framework               equivalent minimal
                                                  dashboard

  Conference/journal      Manuscript preparation  Produce a reproducible
  submission              is feasible; acceptance research manuscript and
                          is not predictable      assess publication
                                                  suitability afterward
  -----------------------------------------------------------------------

**Overall assessment: feasible, provided we freeze a narrow research
question immediately and resist feature expansion.**

I would not promise that the project will be conference-ready in 10
days. We can produce a complete manuscript with a defensible methodology
and measured results, but its novelty and suitability for publication
will depend on what the experiments establish and how it compares with
existing work.

# 2. Reconsidering the research direction

I would change the project from **physical active vision to
sensor-guided adaptive video processing**.

The reason is not simply that it is easier. It gives us a more direct
connection between real video, algorithmic optimization, simulated
sensors, and measurable resource savings.

There is also a research consideration. Adaptive video sampling is
already an active area: a June 2026 paper describes a system that
dynamically chooses between full inference, feature warping, and reusing
previous results on CPU-constrained devices. Other work has explored
scheduling camera observations to maximize event detection. We should
not claim that adaptive sampling or sensor-guided scheduling is itself a
novel invention. [Research reference: adaptive video
processing](https://gr-journals.com/journals/ictasa/issues/v2i2/26310)

Instead, we should define a narrower experimental contribution that your
team can implement and evaluate properly.

## Proposed direction: sensor-guided adaptive video sampling

**Working title**

SAGE: Sensor-Guided Adaptive Video Sampling for Resource-Constrained
Edge Intelligence

### Research question

> Under a fixed computational budget, how do sensor-triggered and
> adaptive video-sampling policies compare with conventional fixed-rate
> sampling in terms of event-detection performance, processing cost, and
> detection latency, particularly when sensor cues are noisy or delayed?

This is a better fit for your current constraints because:

-   It uses **real video**, satisfying the need for substantive DIP/CV.
-   Sensor inputs can be simulated reproducibly.
-   Scheduling and resource allocation remain central to DAA.
-   It requires no physical camera movement or mechanical fabrication.
-   Results can be generated automatically and displayed in a dashboard.
-   The experiment can be repeated with different event rates, sensor
    error rates, and computational budgets.

The research contribution would be the **systematic evaluation of
sensor-guided sampling policies under controlled resource constraints**,
not a claim that you have invented a new computer-vision model.

That distinction matters if you later submit the work to a conference or
journal.

------------------------------------------------------------------------

# 3. What the final system will do

The system will process a real video sequence while a simulation
generates sensor-event streams corresponding to activity in the
environment.

The scheduler determines when the next video frame should receive
detailed processing.

For example:

-   When the scene appears inactive and no sensor cue is present, the
    system samples infrequently.
-   When a simulated sensor reports activity, the system increases its
    sampling rate.
-   When visual activity is detected, the system can temporarily
    allocate more processing.
-   When sensor cues are false positives, the system may waste
    computation.
-   When sensor cues are delayed or miss events, the system may miss or
    detect events late.

These competing effects are precisely what we want to measure.

## Proposed architecture

``` text
                    REAL VIDEO INPUT
                           |
                           v
                  Video Frame Reader
                           |
                           v
                  Frame Sampling Policy
                           |
               +-----------+-----------+
               |                       |
               v                       v
       Simulated Sensor          Sampling Decision
            Engine                     |
               |                       v
               |               OpenCV Processing
               |                       |
               |                       v
               |                Motion Detection
               |                       |
               +----------+------------+
                          |
                          v
                 Experiment Logger
                          |
                          v
                 Metrics and Analysis
                          |
                          v
                 Interactive Dashboard
```

The system will support replaying the same video and simulated sensor
events under different policies. This is important because it allows
fair comparisons using identical inputs.

**Important qualification:** simulated sensor events are not equivalent
to measurements from physical sensors. The paper must describe them as
simulated inputs, not real sensor observations.

------------------------------------------------------------------------

# 4. How we will make the DAA component substantial

The DAA component will be the scheduling problem, not merely the use of
a motion-detection algorithm.

I recommend implementing four policies.

  -----------------------------------------------------------------------
  Policy                  Description             Purpose
  ----------------------- ----------------------- -----------------------
  1\. Fixed-rate sampling Process every (k)-th    Baseline for resource
                          frame                   usage and detection

  2\. Periodic adaptive   Change sampling         Tests a simple adaptive
  sampling                frequency according to  strategy
                          observed activity       

  3\. Sensor-triggered    Increase sampling       Measures the value and
  sampling                frequency when          limitations of sensor
                          simulated sensor events cues
                          arrive                  

  4\. Budget-aware        Allocate processing     Proposed policy to
  adaptive sampling       according to activity,  evaluate
                          sensor confidence, and  
                          remaining budget        
  -----------------------------------------------------------------------

The fourth policy is the research candidate. It should remain simple
enough to implement and explain.

We should not commit to a sophisticated machine-learning predictor
before establishing that a well-designed rule-based policy improves on
the baselines.

### Complexity analysis

For a video containing (F) frames:

-   Fixed-rate sampling processes approximately (F/k) frames.
-   Periodic adaptive sampling has scheduling overhead proportional to
    the number of sampling decisions, in addition to the cost of
    processing selected frames.
-   Sensor-triggered sampling incurs sensor-event handling and
    scheduling overhead.
-   Budget-aware scheduling must account for its policy-specific
    decision and update costs.

For each implementation, we will distinguish **algorithmic scheduling
complexity** from **image-processing cost**. These are different
quantities and should not be conflated.

We will analyze the relevant operations in terms of video frames, sensor
events, and any data structures used by the scheduler.

### Benchmarking

The policies will be evaluated using the same video clips and, where
applicable, the same simulated sensor-event streams.

The main measurements will be:

1.  Event-detection recall.
2.  Event-detection precision.
3.  Detection latency.
4.  Number of frames processed.
5.  Processing time.
6.  Scheduling overhead.
7.  Resource cost relative to the fixed-rate baseline.

The primary result should be a trade-off between **event-detection
quality and processing cost**.

We should not assume the proposed policy will win every metric. If it
saves computation but increases detection latency, that is a legitimate
experimental result.

------------------------------------------------------------------------

# 5. Making the computer-vision component legitimate

The CV pipeline will use actual video and demonstrate explicit
image-processing operations.

I recommend a classical OpenCV pipeline rather than making a
deep-learning model mandatory.

OpenCV supports background subtraction for identifying foreground motion
against a modeled background, making it a reasonable starting point for
this project. [OpenCV background-subtraction
tutorial](https://github.com/opencv/opencv/blob/5.x/doc/tutorials/others/background_subtraction.markdown)

The pipeline will include:

-   Frame acquisition and sampling.
-   Resizing and grayscale conversion.
-   Gaussian filtering.
-   Frame differencing or background subtraction.
-   Thresholding and morphological operations.
-   Motion-region extraction.
-   Event detection and evaluation against ground truth.

We should compare at least two visual-processing approaches if time
permits.

For example, frame differencing and background subtraction have
different computational and detection characteristics. That gives the CV
evaluation some depth without introducing an unnecessary model-training
dependency.

### Ground truth is essential

We must define what constitutes an event in each video and how its start
and end are established.

Possible sources include manually annotated intervals or controlled
recordings of simple motion events.

We must also decide how an event is counted as detected. A defensible
rule might require the detector to report activity within a specified
time window around the annotated event.

Without ground truth, we can report processing speed and frame counts,
but we cannot credibly claim improved event-detection accuracy.

------------------------------------------------------------------------

# 6. How the six subjects map to this revised scope

  -----------------------------------------------------------------------
  Subject                 Primary deliverable     Evidence of completion
  ----------------------- ----------------------- -----------------------
  DAA                     Four scheduling         Complexity derivations,
                          policies and their      benchmark results,
                          analysis                comparisons

  Sensors &               Simulated sensor-event  Event timing, noise,
  Microcontrollers        generator               false-positive and
                                                  missed-event models

  DIP/CV                  Real-video              Image-processing
                          motion-detection        stages, detections,
                          pipeline                ground-truth evaluation

  Software Engineering    Modular, tested         Requirements,
                          software system         architecture, UML, Git
                                                  history, test results

  Embedded Systems        Resource-constrained    Sampling budgets,
                          edge-processing model   processing-time
                                                  measurements,
                                                  scheduling constraints

  PBL                     Integrated research     Dashboard, reproducible
                          prototype               experiments, report and
                                                  demonstration
  -----------------------------------------------------------------------

There is one limitation worth making explicit.

**The revised project can demonstrate embedded-system design concepts,
but simulation alone does not prove real-time performance on the
Raspberry Pi or validate physical sensor integration.** If the Embedded
Systems professor requires a physical implementation or a particular
low-level technique, the current scope may need adjustment.

You have said simulation is acceptable for the sensor requirement, so I
will proceed on that basis.

------------------------------------------------------------------------

# 7. What is inside and outside the 10-day scope

## Mandatory

-   A working Python application.
-   Real-video input.
-   Explicit DIP operations.
-   At least two evaluated visual-processing methods, if feasible within
    the initial implementation.
-   Four scheduling policies.
-   A reproducible sensor-event simulator.
-   Configurable computational budgets and sensor noise.
-   Automated experiments.
-   Quantitative results and plots.
-   An interactive dashboard.
-   Unit and integration tests.
-   Software Engineering documentation.
-   An IEEE-structured research manuscript.

## Explicitly excluded from the critical path

-   Physical camera movement.
-   Servo mechanisms.
-   Real sensor hardware integration.
-   Training a new deep-learning model from scratch.
-   Cloud deployment.
-   Complex multi-user interfaces.
-   Claims of novel computer-vision architecture.
-   Claims of measured Pi 4 performance unless we actually benchmark on
    that device.

We can add a small Raspberry Pi performance test if time and access
permit, but the main experiment must not depend on it.

------------------------------------------------------------------------

# 8. The paper and publication strategy

I recommend preparing the manuscript using IEEE structure from the
beginning.

The paper should contain:

1.  Abstract.
2.  Introduction and problem statement.
3.  Related work.
4.  System model and problem formulation.
5.  Scheduling algorithms.
6.  Experimental methodology.
7.  Results and comparative analysis.
8.  Threats to validity and limitations.
9.  Conclusion and future work.
10. References.

The paper's strongest possible contribution is an experimentally
supported answer to this question:

> **When do simulated sensor cues improve adaptive video-processing
> efficiency, and how sensitive is that improvement to sensor noise,
> event frequency, and processing budget?**

That is more specific and testable than simply claiming that adaptive
video processing is better than fixed-rate processing.

The literature review must determine whether the particular combination
and evaluation methodology offer enough novelty for a target venue. We
should not promise acceptance, and we should not invent a novelty claim
before comparing the final method with relevant prior work.

------------------------------------------------------------------------

# 9. Final scope decision

My recommendation is to **replace the physical active-vision design with
sensor-guided adaptive video sampling**.

It preserves the strongest part of the original idea---the allocation of
limited observation resources---while eliminating mechanical
dependencies and keeping real video at the center of the experiment.

The final research system will have three tightly integrated elements:

1.  **Real-video computer vision** to establish what visual activity is
    detected.
2.  **A simulated sensor environment and scheduling engine** to decide
    when processing should occur.
3.  **A reproducible experimental framework and dashboard** to compare
    the policies quantitatively.

This is the scope I would freeze for the 10-day deadline, subject to one
final qualification: the exact event definition and ground-truth
strategy must be settled before the experiments can be considered
scientifically valid.

## Before implementation begins

I do not need more general project-preference questions. There are only
two facts that could materially change the feasibility assessment:

1.  **Do you already have suitable video clips available**, or must we
    identify and obtain a public dataset or record our own clips?
2.  **Does any professor require a specific embedded-systems technique
    or artifact** beyond the simulation being acceptable for sensors?

If the answer to the second question is unknown, we can proceed with the
current scope and explicitly document the assumption. Once these two
points are resolved, the project direction can be frozen and the
implementation work can be coordinated through your central Codex
workflow and separate SAGE Project chats.

------------------------------------------------------------------------

## Decision register and assumptions

This register separates the current scope recommendation from details
that still require confirmation.

  --------------------------------------------------------------------------------------------
  ID                Decision or        Status            Notes
                    assumption                           
  ----------------- ------------------ ----------------- -------------------------------------
  D-01              Use sensor-guided  Recommended;      Preserves the
                    adaptive video     freeze after open allocation-of-observation-resources
                    sampling rather    questions are     idea while avoiding mechanical
                    than physical      addressed         dependencies.
                    active vision as                     
                    the main                             
                    direction.                           

  D-02              Use real video for Required          The dataset and event annotations
                    the                                  still need to be selected.
                    computer-vision                      
                    pipeline.                            

  D-03              Simulate           Accepted working  Simulated inputs must not be
                    sensor-event       assumption        described as physical sensor
                    streams and sensor                   measurements.
                    noise.                               

  D-04              Compare four       Required          Fixed-rate, periodic adaptive,
                    scheduling                           sensor-triggered, and budget-aware
                    policies.                            adaptive.

  D-05              Use a lightweight  Required          Streamlit is the suggested default,
                    interactive                          not a hard dependency if an
                    dashboard.                           equivalent is more practical.

  D-06              Prepare an         Required          Submission suitability and acceptance
                    IEEE-structured    deliverable       are not guaranteed.
                    manuscript.                          

  A-01              The project can be Planning          Must be reviewed against actual
                    completed within   assumption        progress and dataset availability.
                    the 10-day window                    
                    if scope is                          
                    controlled.                          

  A-02              Simulation is      Assumed from      Confirm whether any separate
                    acceptable for the current project   embedded-systems artifact is
                    Sensors &          guidance          compulsory.
                    Microcontrollers                     
                    component.                           

  A-03              Classical OpenCV   Recommended       Do not add model training unless the
                    methods are                          core experiment is already working.
                    sufficient for the                   
                    initial                              
                    implementation.                      

  A-04              Hardware           Binding reporting Do not present simulated resource
                    performance claims constraint        budgets as measured Raspberry Pi
                    are out of scope                     performance.
                    unless directly                      
                    measured.                            
  --------------------------------------------------------------------------------------------

## Open questions

Resolve these before finalizing the experimental protocol.

-   [ ] **Video availability:** Are suitable video clips already
    available, or must the team obtain a public dataset or record clips?
-   [ ] **Embedded Systems requirements:** Does the professor require a
    specific technique, hardware artifact, low-level implementation, or
    Raspberry Pi demonstration beyond simulation?
-   [ ] **Event definition:** What constitutes an event for the chosen
    video domain, and how will its start and end be annotated?
-   [ ] **Ground-truth source:** Will annotations be created manually,
    taken from a suitable dataset, or generated from controlled
    recordings?
-   [ ] **Detection matching rule:** What time window or overlap rule
    will count a detection as a true positive?
-   [ ] **Experimental budget:** Which computational budgets, sampling
    intervals, sensor false-positive rates, missed-event rates, and
    delays will be tested?
-   [ ] **Target venue:** Which conference or journal, if any, will be
    considered after the related-work review and results are available?

If a professor's requirement is unknown, record it as an unresolved
assumption rather than treating it as confirmed.

## Acceptance criteria

The project should not be considered complete merely because the
dashboard runs. The following criteria define the minimum evidence
expected from the integrated system.

### Functional criteria

-   [ ] The application loads and processes at least one suitable real
    video clip.
-   [ ] The computer-vision pipeline performs documented
    image-processing operations.
-   [ ] All four scheduling policies can be selected and executed.
-   [ ] The sensor simulator supports configurable event timing and
    noise parameters.
-   [ ] The experiment runner can replay the same video and sensor-event
    inputs across policies.
-   [ ] The system records experiment settings, detections, and metric
    outputs.
-   [ ] The dashboard displays comparable results for the tested
    policies.
-   [ ] The project can be installed and run from documented setup
    instructions.

### Research and evaluation criteria

-   [ ] Ground-truth events and the detection-matching rule are
    explicitly defined.
-   [ ] Precision, recall, detection latency, frames processed,
    processing time, scheduling overhead, and relative resource cost are
    reported where applicable.
-   [ ] At least one baseline comparison is reproducible; the planned
    comparison includes all four policies.
-   [ ] Results include plots or tables and are interpreted without
    assuming the proposed policy must win.
-   [ ] Algorithmic scheduling complexity is distinguished from
    image-processing cost.
-   [ ] Limitations, simulation assumptions, and threats to validity are
    documented.
-   [ ] Related work is reviewed before making any novelty claim.

### Engineering and academic criteria

-   [ ] The repository contains clear setup instructions and dependency
    specifications.
-   [ ] Unit and integration tests cover core behavior and the main
    experiment path.
-   [ ] Architecture and required Software Engineering documentation are
    included.
-   [ ] The IEEE-structured manuscript reports the methodology and
    actual measured results.
-   [ ] No claim of physical sensor integration, Raspberry Pi
    performance, or publication readiness is made without supporting
    evidence.

## Implementation checklist

Use this as a short execution checklist for the 10-day window. Adjust
sequencing when dataset access or professor requirements demand it.

### Scope and experimental design

-   [ ] Resolve the open questions that could materially change
    feasibility.
-   [ ] Select video clips and establish event ground truth.
-   [ ] Define metrics, detection-matching rules, and experimental
    parameter ranges.
-   [ ] Record the final scope and any remaining assumptions.

### Core implementation

-   [ ] Build video input and frame-sampling interfaces.
-   [ ] Implement and test the initial OpenCV motion-detection pipeline.
-   [ ] Implement the simulated sensor-event generator.
-   [ ] Implement the four scheduling policies.
-   [ ] Add configurable processing budgets and sensor-noise parameters.
-   [ ] Build a reproducible experiment runner and structured result
    logging.

### Evaluation and interface

-   [ ] Run the same inputs across all policies.
-   [ ] Calculate the agreed metrics and generate comparison plots.
-   [ ] Check results for inconsistencies and rerun failed or
    non-reproducible experiments.
-   [ ] Build the dashboard around the experiment outputs.
-   [ ] Demonstrate at least one complete end-to-end experiment.

### Quality and reporting

-   [ ] Add unit and integration tests.
-   [ ] Complete setup instructions, architecture documentation, and
    required UML artifacts.
-   [ ] Review related work and refine the contribution claim.
-   [ ] Write the manuscript using the actual methodology and results.
-   [ ] Document limitations and distinguish simulated results from
    hardware measurements.
-   [ ] Perform a final clean-environment run from the repository
    instructions.

## References

-   [Research reference: adaptive video
    processing](https://gr-journals.com/journals/ictasa/issues/v2i2/26310)
    --- cited in the source discussion as an example of existing
    adaptive video-processing work. Verify bibliographic details and
    relevance during the formal literature review.
-   [OpenCV background-subtraction
    tutorial](https://github.com/opencv/opencv/blob/5.x/doc/tutorials/others/background_subtraction.markdown)
    --- technical reference for the proposed classical computer-vision
    pipeline.

> **Reference quality note:** These are the links carried forward from
> the source document, with tracking parameters removed and link text
> clarified. They have not been independently verified as a complete
> literature review. Verify each source and add primary research
> references before finalizing the manuscript.
