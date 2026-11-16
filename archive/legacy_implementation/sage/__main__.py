"""Entry point: ``python -m sage`` and ``python -m sage demo``."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from .cli import main as run_cli
from .engine import (ExperimentConfig, Event, load_frames, run_experiment,
                     write_event_results, write_results, write_trace)


def demo(output_dir: str = "outputs/demo") -> None:
    """Generate a small synthetic sequence and run all policies without downloads."""
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
    except ImportError as exc:
        raise SystemExit("Install requirements.txt to run the synthetic demo") from exc
    root = Path(output_dir)
    frame_dir = root / "synthetic_frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    fps, count = 10.0, 70
    for i in range(count):
        image = np.zeros((240, 320, 3), dtype=np.uint8)
        image[:] = (30, 35, 40)
        cv2.rectangle(image, (0, 175), (319, 239), (70, 70, 70), -1)
        if 12 <= i <= 32:
            x = 20 + (i - 12) * 10
            cv2.rectangle(image, (x, 125), (x + 32, 174), (0, 190, 240), -1)
        if 48 <= i <= 58:
            cv2.circle(image, (70 + 12 * (i - 48), 145), 18, (40, 200, 40), -1)
        cv2.imwrite(str(frame_dir / f"frame_{i:04d}.png"), image)
    event_file = root / "events.csv"
    with event_file.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["start_s", "end_s", "label"])
        writer.writerow([1.2, 3.2, "moving_object"])
        writer.writerow([4.8, 5.9, "second_motion_event"])
    frames, _ = load_frames(frame_dir, fps)
    trace: list[dict] = []
    per_event: list[dict] = []
    rows = run_experiment(frames, fps, [Event(1.2, 3.2, "moving_object"), Event(4.8, 5.9, "second_motion_event")],
                          ExperimentConfig(warmup_frames=0), "synthetic_demo", trace, "synthetic_demo", per_event)
    csv_path, jsonl_path = write_results(rows, root)
    trace_path, _ = write_trace(trace, root)
    event_csv_path, _ = write_event_results(per_event, root)
    print(json.dumps({"data_source": "synthetic_demo", "frames": count, "fps": fps,
                      "csv": str(csv_path), "jsonl": str(jsonl_path), "frame_trace": str(trace_path),
                      "event_results": str(event_csv_path), "event_annotations": str(event_file)}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        parser = argparse.ArgumentParser(description="Run a deterministic synthetic SAGE demo")
        parser.add_argument("demo")
        parser.add_argument("--output", default="outputs/demo")
        demo(parser.parse_args().output)
    else:
        run_cli()
