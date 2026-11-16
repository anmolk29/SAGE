"""Reproducible, simulation-first SAGE experiment engine.

The engine intentionally separates public video, human supplied event intervals,
and simulated sensor cues. Software time is measured locally; no hardware energy
or edge-device performance is inferred.
"""

from __future__ import annotations

import csv
import json
import math
import random
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover - exercised on minimal installs
    cv2 = None
    np = None


POLICIES = ("fixed_rate", "video_adaptive", "sensor_triggered", "budget_aware")
DETECTORS = ("motion", "hog_people", "resnet18_probe")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


@dataclass(frozen=True)
class Event:
    """Ground-truth event interval in seconds; labels are descriptive only."""

    start_s: float
    end_s: float
    label: str = "event"

    def __post_init__(self) -> None:
        if self.start_s < 0 or self.end_s < self.start_s:
            raise ValueError("Event requires 0 <= start_s <= end_s")


@dataclass(frozen=True)
class SimulationConfig:
    """Sensor quality controls. All values describe a simulator, not hardware."""

    event_detection_probability: float = 0.9
    false_triggers_per_minute: float = 0.2
    delay_s: float = 0.0
    seed: int = 7

    def __post_init__(self) -> None:
        if not 0 <= self.event_detection_probability <= 1:
            raise ValueError("event_detection_probability must be in [0, 1]")
        if self.false_triggers_per_minute < 0 or self.delay_s < 0:
            raise ValueError("false trigger rate and delay must be non-negative")


@dataclass(frozen=True)
class ExperimentConfig:
    detector: str = "motion"
    model_path: str | None = None
    head_path: str | None = None
    policies: tuple[str, ...] = POLICIES
    fixed_stride: int = 5
    low_stride: int = 10
    high_stride: int = 1
    motion_threshold: float = 0.015
    budget_fraction: float = 0.25
    sensor_window_s: float = 2.0
    warmup_frames: int = 3
    simulation: SimulationConfig = field(default_factory=SimulationConfig)

    def __post_init__(self) -> None:
        if self.detector not in DETECTORS:
            raise ValueError(f"detector must be one of {DETECTORS}")
        if self.detector == "resnet18_probe" and (not self.model_path or not self.head_path):
            raise ValueError("resnet18_probe requires model_path and head_path")
        if not self.policies or any(p not in POLICIES for p in self.policies):
            raise ValueError(f"policies must be selected from {POLICIES}")
        if min(self.fixed_stride, self.low_stride, self.high_stride) < 1:
            raise ValueError("sampling strides must be >= 1")
        if not 0 < self.budget_fraction <= 1:
            raise ValueError("budget_fraction must be in (0, 1]")


def _natural_key(path: Path) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", path.name)]


def load_frames(source: str | Path, fps_override: float | None = None) -> tuple[list[Any], float]:
    """Load a video or a directory of ordered image frames.

    Returns (BGR frames, frames per second). Sequence directories use a 1 FPS
    default because original timestamps may be absent; callers should pass the
    documented rate explicitly. Video files use their container's reported rate.
    """
    if cv2 is None:
        raise RuntimeError("OpenCV is required. Install requirements.txt first.")
    path = Path(source)
    if path.is_dir():
        files = sorted((p for p in path.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES), key=_natural_key)
        frames = [cv2.imread(str(p)) for p in files]
        frames = [frame for frame in frames if frame is not None]
        if not frames:
            raise ValueError(f"No readable image frames in {path}")
        return frames, float(fps_override or 1.0)
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise ValueError(f"Could not open video: {path}")
    fps = fps_override or capture.get(cv2.CAP_PROP_FPS) or 1.0
    frames = []
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            frames.append(frame)
    finally:
        capture.release()
    if not frames:
        raise ValueError(f"No frames found in video: {path}")
    return frames, float(fps)


def load_events(path: str | Path) -> list[Event]:
    """Read CSV columns start_s,end_s[,label]."""
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"start_s", "end_s"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Event CSV needs start_s and end_s columns")
        return [Event(float(row["start_s"]), float(row["end_s"]), row.get("label") or "event")
                for row in reader]


def simulate_sensor_cues(events: Sequence[Event], duration_s: float,
                         config: SimulationConfig) -> list[float]:
    """Generate reproducible imperfect triggers from event intervals plus noise."""
    rng = random.Random(config.seed)
    cues = [event.start_s + config.delay_s for event in events
            if rng.random() <= config.event_detection_probability]
    count = rng.poissonvariate(config.false_triggers_per_minute * duration_s / 60) if hasattr(rng, "poissonvariate") else None
    # Python's Random has no Poisson sampler; a Bernoulli process per second keeps
    # expected false-trigger count controlled and is deterministic for a seed.
    if count is None:
        rate = config.false_triggers_per_minute / 60.0
        for second in range(math.ceil(duration_s)):
            if rng.random() < min(rate, 1.0):
                cues.append(min(duration_s, second + rng.random()))
    return sorted(max(0.0, cue) for cue in cues if cue <= duration_s)


class _MotionDetector:
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.previous = None
        self.background = cv2.createBackgroundSubtractorMOG2(history=120, varThreshold=32, detectShadows=False)

    def __call__(self, frame: Any, index: int) -> tuple[bool, float]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 240))
        foreground = self.background.apply(gray, learningRate=0.01 if index > 3 else 0.1)
        score = float(np.count_nonzero(foreground) / foreground.size)
        return score >= self.threshold, score


class _HogPeopleDetector:
    """OpenCV's pretrained default HOG+linear-SVM pedestrian detector."""

    def __init__(self):
        self.model = cv2.HOGDescriptor()
        self.model.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def __call__(self, frame: Any, index: int) -> tuple[bool, float]:
        resized = cv2.resize(frame, (640, max(128, round(frame.shape[0] * 640 / frame.shape[1]))))
        boxes, weights = self.model.detectMultiScale(resized, winStride=(8, 8), padding=(8, 8), scale=1.05)
        return bool(len(boxes)), float(max(weights)) if len(weights) else 0.0


def _detections(frames: Sequence[Any], selected: Sequence[int], detector_name: str,
                threshold: float, warmup_frames: int, model_path: str | None = None,
                head_path: str | None = None, detector_instance: Any | None = None
                ) -> tuple[dict[int, tuple[bool, float]], float]:
    if detector_instance is not None:
        detector = detector_instance
    elif detector_name == "motion":
        detector = _MotionDetector(threshold)
    elif detector_name == "hog_people":
        detector = _HogPeopleDetector()
    else:
        from .ml import ResNet18LinearProbeDetector
        if not model_path or not head_path:
            raise ValueError("resnet18_probe requires model_path and head_path")
        detector = ResNet18LinearProbeDetector(model_path, head_path)
    results: dict[int, tuple[bool, float]] = {}
    started = time.perf_counter()
    for idx in selected:
        detected, score = detector(frames[idx], idx)
        if idx < warmup_frames and detector_name == "motion":
            detected = False
        results[idx] = (detected, score)
    return results, time.perf_counter() - started


def _select_frames(policy: str, frame_count: int, fps: float,
                   config: ExperimentConfig, cues: Sequence[float],
                   motion_scores: Sequence[float] | None = None) -> list[int]:
    """Select an exact common quota with causal signals and deterministic fallback."""
    quota = min(frame_count, max(1, math.ceil(frame_count * config.budget_fraction)))
    if policy == "fixed_rate":
        # Uniformly spread q indices across N using integer arithmetic.
        return [(k * frame_count) // quota for k in range(quota)]
    selected: list[int] = []
    active_until = -1
    cue_idx = 0
    for i in range(frame_count):
        now = i / fps
        while cue_idx < len(cues) and cues[cue_idx] <= now:
            active_until = max(active_until, round((cues[cue_idx] + config.sensor_window_s) * fps))
            cue_idx += 1
        remaining_quota = quota - len(selected)
        remaining_frames = frame_count - i
        if remaining_quota <= 0:
            take = False
        elif remaining_quota == remaining_frames:
            take = True
        else:
            motion_active = motion_scores is not None and motion_scores[i] >= config.motion_threshold
            cue_active = i <= active_until
            if policy == "video_adaptive":
                signal = motion_active
            elif policy == "sensor_triggered":
                signal = cue_active
            elif policy == "budget_aware":
                signal = motion_active or cue_active
            else:
                raise ValueError(f"unknown policy: {policy}")
            # Favor current signals, otherwise spread the remaining quota evenly.
            fallback_stride = max(1, math.ceil(remaining_frames / remaining_quota))
            take = signal or (i % fallback_stride == 0)
        if take:
            selected.append(i)
    if len(selected) != quota:
        raise RuntimeError(f"{policy} selected {len(selected)} frames; expected quota {quota}")
    return selected


def _event_metrics(events: Sequence[Event], detections: Sequence[float], duration_s: float) -> dict[str, Any]:
    detected = 0
    latencies: list[float] = []
    false_count = 0
    for event in events:
        hits = [t for t in detections if event.start_s <= t <= event.end_s]
        if hits:
            detected += 1
            latencies.append(hits[0] - event.start_s)
    false_count = sum(not any(e.start_s <= t <= e.end_s for e in events) for t in detections)
    return {
        "event_count": len(events),
        "events_detected": detected,
        "event_recall": detected / len(events) if events else None,
        "false_alarms": false_count,
        "false_alarms_per_minute": false_count / (duration_s / 60) if duration_s > 0 else 0.0,
        "mean_detection_latency_s": sum(latencies) / len(latencies) if latencies else None,
        "missed_events": len(events) - detected,
    }


def run_experiment(frames: Sequence[Any], fps: float, events: Sequence[Event],
                   config: ExperimentConfig | None = None,
                   clip_id: str = "clip",
                   trace_rows: list[dict[str, Any]] | None = None,
                   data_source: str = "user_provided",
                   event_rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Run selected policies on one clip and return one reproducible metric row each."""
    if cv2 is None or np is None:
        raise RuntimeError("OpenCV and NumPy are required. Install requirements.txt first.")
    if not frames or fps <= 0:
        raise ValueError("frames must be non-empty and fps must be positive")
    cfg = config or ExperimentConfig()
    duration = len(frames) / fps
    cues = simulate_sensor_cues(events, duration, cfg.simulation)
    # The video-adaptive and budget-aware policies use a lightweight MOG2 scout on
    # every frame. Report that pass separately and charge it to each affected row;
    # selected-frame detector runtime remains separately measurable.
    scout_runtime = 0.0
    motion_scores = [0.0] * len(frames)
    if any(p in ("video_adaptive", "budget_aware") for p in cfg.policies):
        scout = _MotionDetector(cfg.motion_threshold)
        scout_started = time.perf_counter()
        for i, frame in enumerate(frames):
            _, motion_scores[i] = scout(frame, i)
        scout_runtime = time.perf_counter() - scout_started
    shared_detector = None
    if cfg.detector == "resnet18_probe":
        from .ml import ResNet18LinearProbeDetector
        shared_detector = ResNet18LinearProbeDetector(cfg.model_path, cfg.head_path)
    output = []
    for policy in cfg.policies:
        selected = _select_frames(policy, len(frames), fps, cfg, cues, motion_scores)
        observed, detector_runtime = _detections(
            frames, selected, cfg.detector, cfg.motion_threshold, cfg.warmup_frames,
            cfg.model_path, cfg.head_path, shared_detector)
        charged_scout_runtime = scout_runtime if policy in ("video_adaptive", "budget_aware") else 0.0
        runtime = detector_runtime + charged_scout_runtime
        if trace_rows is not None:
            chosen = set(selected)
            for idx in range(len(frames)):
                hit = observed.get(idx)
                now = idx / fps
                cue_active = any(c <= now <= c + cfg.sensor_window_s for c in cues)
                trace_rows.append({
                    "clip": clip_id, "policy": policy, "frame_idx": idx, "time_s": now,
                    "selected": idx in chosen,
                    "detected": hit[0] if hit else None,
                    "detector_score": hit[1] if hit else None,
                    "sensor_cue_active": cue_active,
                })
        detected_times = [idx / fps for idx, (detected, _) in observed.items() if detected]
        if event_rows is not None:
            for event_index, event in enumerate(events, start=1):
                valid_hits = [t for t in detected_times if event.start_s <= t <= event.end_s]
                first_hit = min(valid_hits) if valid_hits else None
                event_rows.append({
                    "clip": clip_id,
                    "policy": policy,
                    "detector": cfg.detector,
                    "event_index": event_index,
                    "event_type": event.label,
                    "start_s": event.start_s,
                    "end_s": event.end_s,
                    "detected": bool(valid_hits),
                    "missed": not bool(valid_hits),
                    "first_detection_time_s": first_hit,
                    "detection_latency_s": first_hit - event.start_s if first_hit is not None else None,
                    "seed": cfg.simulation.seed,
                    "budget": cfg.budget_fraction,
                    "cue_detection_probability": cfg.simulation.event_detection_probability,
                    "false_trigger_rate": cfg.simulation.false_triggers_per_minute,
                    "cue_delay_seconds": cfg.simulation.delay_s,
                })
        row = {
            "clip": clip_id,
            "clip_id": clip_id,
            "source_id": clip_id,
            "data_source": data_source,
            "policy": policy,
            "detector": cfg.detector,
            "model_name": ({"motion": "OpenCV MOG2 background subtraction",
                            "hog_people": "OpenCV default HOG + linear-SVM pedestrian detector",
                            "resnet18_probe": "ImageNet ResNet-18 logits + clip-trained logistic probe"}[cfg.detector]),
            "model_path": cfg.model_path,
            "head_path": cfg.head_path,
            "opencv_version": cv2.__version__,
            "numpy_version": np.__version__,
            "budget": cfg.budget_fraction,
            "frames_total": len(frames),
            "total_frames": len(frames),
            "frames_analyzed": len(selected),
            "frames_fraction": len(selected) / len(frames),
            "fps": fps,
            "duration_s": duration,
            "software_runtime_s": runtime,
            "processing_time_seconds": runtime,
            "scout_frames": len(frames) if charged_scout_runtime else 0,
            "scout_runtime_seconds": charged_scout_runtime,
            "detector_runtime_seconds": detector_runtime,
            "sensor_simulated": True,
            "sensor_event_detection_probability": cfg.simulation.event_detection_probability,
            "cue_detection_probability": cfg.simulation.event_detection_probability,
            "sensor_false_triggers_per_minute": cfg.simulation.false_triggers_per_minute,
            "false_trigger_rate": cfg.simulation.false_triggers_per_minute,
            "sensor_delay_s": cfg.simulation.delay_s,
            "cue_delay_seconds": cfg.simulation.delay_s,
            "sensor_seed": cfg.simulation.seed,
            "seed": cfg.simulation.seed,
            "target_budget_fraction": cfg.budget_fraction,
            "target_frames": math.ceil(len(frames) * cfg.budget_fraction),
            "budget_fraction": cfg.budget_fraction,
            **_event_metrics(events, detected_times, duration),
        }
        row["mean_latency_seconds"] = row["mean_detection_latency_s"]
        row["events_total"] = row["event_count"]
        output.append(row)
    return output


def run_ablation(frames: Sequence[Any], fps: float, events: Sequence[Event],
                 base: ExperimentConfig | None = None,
                 clip_id: str = "clip",
                 trace_rows: list[dict[str, Any]] | None = None,
                 event_rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Run paired ablations over cue reliability, noise, and delay settings."""
    base = base or ExperimentConfig()
    conditions = [
        ("reliable", 1.0, 0.0, 0.0),
        ("misses", 0.5, 0.0, 0.0),
        ("false_triggers", 1.0, 2.0, 0.0),
        ("delay", 1.0, 0.0, 1.0),
        ("no_sensor", 0.0, 0.0, 0.0),
    ]
    rows = []
    for name, probability, false_rate, delay in conditions:
        cfg = ExperimentConfig(**{
            **asdict(base),
            "simulation": SimulationConfig(probability, false_rate, delay, base.simulation.seed),
        })
        condition_trace: list[dict[str, Any]] = []
        condition_events: list[dict[str, Any]] = []
        for row in run_experiment(frames, fps, events, cfg, clip_id, condition_trace,
                                  event_rows=condition_events):
            rows.append({**row, "ablation": name})
        if trace_rows is not None:
            trace_rows.extend({**trace_row, "ablation": name} for trace_row in condition_trace)
        if event_rows is not None:
            event_rows.extend({**event_row, "ablation": name} for event_row in condition_events)
    return rows


def write_results(rows: Iterable[dict[str, Any]], output_dir: str | Path) -> tuple[Path, Path]:
    """Write a flat CSV and JSONL with the full experiment settings per row."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    csv_path, jsonl_path = directory / "results.csv", directory / "results.jsonl"
    if rows:
        fields = list(dict.fromkeys(key for row in rows for key in row))
        with csv_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        csv_path.write_text("", encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    return csv_path, jsonl_path


def write_trace(trace_rows: Iterable[dict[str, Any]], output_dir: str | Path) -> tuple[Path, Path]:
    """Persist per-frame scheduling and detector decisions for reproducibility."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    rows = list(trace_rows)
    csv_path, jsonl_path = directory / "frame_trace.csv", directory / "frame_trace.jsonl"
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        if fields:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    with jsonl_path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    return csv_path, jsonl_path


def write_event_results(event_rows: Iterable[dict[str, Any]], output_dir: str | Path) -> tuple[Path, Path]:
    """Write per-event types, detection outcomes, and cue/budget provenance."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    rows = list(event_rows)
    csv_path, jsonl_path = directory / "event_results.csv", directory / "event_results.jsonl"
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        if fields:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    with jsonl_path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    return csv_path, jsonl_path
