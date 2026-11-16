"""Command line runner: python -m sage.cli --help"""

from __future__ import annotations

import argparse
import json

from .engine import (ExperimentConfig, SimulationConfig, load_events, load_frames,
                     run_ablation, run_experiment, write_event_results,
                     write_results, write_trace)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a reproducible SAGE experiment with all policies matched to one frame quota")
    parser.add_argument("--video", required=True, help="video file or directory of ordered image frames")
    parser.add_argument("--events", required=True, help="CSV with start_s,end_s[,label]")
    parser.add_argument("--output", default="outputs/run", help="result directory")
    parser.add_argument("--clip-id", default="clip")
    parser.add_argument("--data-source", default="user_provided", help="source label recorded in run provenance")
    parser.add_argument("--fps", type=float, help="override fps; recommended for image sequences")
    parser.add_argument("--detector", choices=("motion", "hog_people", "resnet18_probe"), default="motion")
    parser.add_argument("--model-path", help="ONNX ResNet-18 ImageNet weights (resnet18_probe only)")
    parser.add_argument("--head-path", help="clip-held-out logistic-head JSON (resnet18_probe only)")
    parser.add_argument("--policies", nargs="+", choices=("fixed_rate", "video_adaptive", "sensor_triggered", "budget_aware"), default=None)
    parser.add_argument("--budget", type=float, default=0.25, help="common target fraction of frames analyzed by every policy (exact quota: ceil(total_frames × fraction))")
    parser.add_argument("--cue-probability", type=float, default=0.9)
    parser.add_argument("--false-triggers-per-minute", type=float, default=0.2)
    parser.add_argument("--cue-delay", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--ablation", action="store_true", help="run the cue-quality ablation matrix")
    args = parser.parse_args()

    frames, fps = load_frames(args.video, args.fps)
    events = load_events(args.events)
    config = ExperimentConfig(
        detector=args.detector,
        model_path=args.model_path,
        head_path=args.head_path,
        policies=tuple(args.policies or ("fixed_rate", "video_adaptive", "sensor_triggered", "budget_aware")),
        budget_fraction=args.budget,
        simulation=SimulationConfig(args.cue_probability, args.false_triggers_per_minute, args.cue_delay, args.seed),
    )
    trace = []
    per_event = []
    rows = run_ablation(frames, fps, events, config, args.clip_id, trace, per_event) if args.ablation else run_experiment(
        frames, fps, events, config, args.clip_id, trace, args.data_source, per_event)
    csv_path, jsonl_path = write_results(rows, args.output)
    trace_path = write_trace(trace, args.output)[0] if trace else None
    event_csv_path = write_event_results(per_event, args.output)[0]
    print(json.dumps({"rows": len(rows), "csv": str(csv_path), "jsonl": str(jsonl_path), "event_results": str(event_csv_path), "frame_trace": str(trace_path) if trace_path else None, "frames": len(frames), "fps": fps}, indent=2))


if __name__ == "__main__":
    main()
