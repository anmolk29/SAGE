"""Train clip-held-out binary heads over frozen ImageNet ResNet-18 logits."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from sage.engine import load_frames
from sage.ml import ResNet18ImageNetEncoder, fit_linear_probe


CLIPS = {
    "wood2": "data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_2_labeled_transition_2250_2455",
    "wood3": "data/derived/mendeley-conveyor/boardcamera_iron_ore_7_wood_3_labeled_transition_2300_2467",
    "things": "data/derived/mendeley-conveyor/boardcamera_iron_ore_things_labeled_transition_2840_3017",
}


def labels_for(root: Path) -> np.ndarray:
    provenance = json.loads((root / "pilot_provenance.json").read_text(encoding="utf-8"))
    ranges = provenance["included_source_frame_ids"]
    frame_ids = sorted((int(path.stem) for path in root.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png"}))
    anomaly_ranges = [value for key, value in ranges.items() if "annomaly" in key.lower() or "anomaly" in key.lower()]
    normal_ranges = [value for key, value in ranges.items() if "normal" in key.lower()]
    labels = []
    for source_id in frame_ids:
        is_anomaly = any(int(bounds[0]) <= source_id <= int(bounds[1]) for bounds in anomaly_ranges)
        is_normal = any(int(bounds[0]) <= source_id <= int(bounds[1]) for bounds in normal_ranges)
        if is_anomaly == is_normal:
            raise ValueError(f"Source frame {source_id} in {root} has ambiguous/missing folder label")
        labels.append(int(is_anomaly))
    return np.asarray(labels, dtype=np.int64)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", default="models/pretrained/resnet18-v1-7.onnx")
    parser.add_argument("--output-dir", default="models/linear-probes")
    parser.add_argument("--cache-dir", default=".codex-build/sage-ml-features")
    args = parser.parse_args()
    model_path = Path(args.model_path)
    output_dir = Path(args.output_dir)
    cache_dir = Path(args.cache_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    encoder = ResNet18ImageNetEncoder(model_path)
    datasets: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for clip_id, directory in CLIPS.items():
        root = Path(directory)
        cache_path = cache_dir / f"{clip_id}_resnet18_imagenet_logits.npz"
        provenance = json.loads((root / "pilot_provenance.json").read_text(encoding="utf-8"))
        fps = float(provenance["derived_fps"])
        frames, fps = load_frames(root, fps_override=fps)
        labels = labels_for(root)
        if labels.size != len(frames):
            raise RuntimeError(f"Frame/label count mismatch for {clip_id}: {len(frames)} vs {labels.size}")
        if cache_path.exists():
            with np.load(cache_path) as cached:
                features = cached["features"]
                cached_labels = cached["labels"]
            if features.shape != (len(frames), 1000) or not np.array_equal(cached_labels, labels):
                cache_path.unlink()
                features = encoder.logits_batch(frames)
                np.savez_compressed(cache_path, features=features, labels=labels)
        else:
            features = encoder.logits_batch(frames)
            np.savez_compressed(cache_path, features=features, labels=labels)
        if features.shape != (len(frames), 1000):
            raise RuntimeError(f"Unexpected ResNet output for {clip_id}: {features.shape}")
        datasets[clip_id] = (features, labels)
        print(f"features {clip_id}: frames={len(frames)} normal={(labels == 0).sum()} anomaly={(labels == 1).sum()}")

    summary = {
        "model": "ONNX Model Zoo ResNet-18 v1-7, ImageNet 1000-class logits as frozen features",
        "model_path": str(model_path),
        "model_sha256": file_sha256(model_path),
        "label_source": "weak/manual folder membership recorded as source-frame ranges in each pilot_provenance.json",
        "validation_design": "leave-one-source-video-out across three selected clips",
        "heads": {},
    }
    for held_out, (test_x, test_y) in datasets.items():
        train_x = np.concatenate([x for clip, (x, _) in datasets.items() if clip != held_out], axis=0)
        train_y = np.concatenate([y for clip, (_, y) in datasets.items() if clip != held_out], axis=0)
        head = fit_linear_probe(train_x, train_y)
        head.update({
            "model_name": "ImageNet ResNet-18 logits + class-balanced logistic linear probe",
            "model_sha256": summary["model_sha256"],
            "held_out_clip": held_out,
            "training_clips": [clip for clip in datasets if clip != held_out],
            "label_source": summary["label_source"],
            "training_frame_count": int(train_y.size),
            "held_out_frame_count": int(test_y.size),
        })
        path = output_dir / f"resnet18_probe_heldout_{held_out}.json"
        path.write_text(json.dumps(head, indent=2), encoding="utf-8")
        summary["heads"][held_out] = {
            "path": str(path),
            "training_clips": head["training_clips"],
            "training_frames": head["training_frame_count"],
            "training_normal": head["normal_examples"],
            "training_anomaly": head["anomaly_examples"],
            "held_out_frames": head["held_out_frame_count"],
        }
        print(f"head {held_out}: train={head['training_frame_count']} held_out={head['held_out_frame_count']} -> {path}")

    (output_dir / "resnet18_probe_cv_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
