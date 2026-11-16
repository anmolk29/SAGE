"""ONNX ResNet-18 feature extraction and weak-label linear probing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np


class ResNet18ImageNetEncoder:
    """ImageNet-pretrained ResNet-18 logits from the Apache-2.0 ONNX Model Zoo."""

    def __init__(self, model_path: str | Path):
        try:
            import onnxruntime as ort  # type: ignore
        except ImportError as exc:  # pragma: no cover - depends on optional package
            raise RuntimeError("Install onnxruntime to use the ResNet-18 probe") from exc
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name

    @staticmethod
    def preprocess(frame: Any) -> np.ndarray:
        height, width = frame.shape[:2]
        scale = 256.0 / min(height, width)
        resized = cv2.resize(frame, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_LINEAR)
        y = (resized.shape[0] - 224) // 2
        x = (resized.shape[1] - 224) // 2
        crop = cv2.cvtColor(resized[y:y + 224, x:x + 224], cv2.COLOR_BGR2RGB).astype(np.float32)
        mean = np.asarray([123.675, 116.28, 103.53], dtype=np.float32)
        std = np.asarray([58.395, 57.12, 57.375], dtype=np.float32)
        return ((crop - mean) / std).transpose(2, 0, 1)

    def logits(self, frame: Any) -> np.ndarray:
        batch = self.preprocess(frame)[None, ...]
        return self.session.run(None, {self.input_name: batch})[0][0].astype(np.float64)

    def logits_batch(self, frames: Sequence[Any], batch_size: int = 16) -> np.ndarray:
        outputs = []
        for start in range(0, len(frames), batch_size):
            batch = np.stack([self.preprocess(frame) for frame in frames[start:start + batch_size]])
            outputs.append(self.session.run(None, {self.input_name: batch})[0].astype(np.float64))
        return np.concatenate(outputs, axis=0) if outputs else np.empty((0, 1000), dtype=np.float64)


def fit_linear_probe(features: np.ndarray, labels: np.ndarray, *, steps: int = 1200,
                     learning_rate: float = 0.04, regularization: float = 0.01) -> dict[str, Any]:
    """Fit a class-balanced logistic head over frozen ImageNet class logits."""
    x = np.asarray(features, dtype=np.float64)
    y = np.asarray(labels, dtype=np.float64).reshape(-1)
    if x.ndim != 2 or x.shape[0] != y.size or x.shape[0] < 2:
        raise ValueError("features must be a 2D array aligned with at least two labels")
    positives = int(np.count_nonzero(y == 1))
    negatives = int(np.count_nonzero(y == 0))
    if positives == 0 or negatives == 0:
        raise ValueError("linear probe training requires both normal and anomaly labels")
    mean = x.mean(axis=0)
    scale = x.std(axis=0)
    scale[scale < 1e-6] = 1.0
    z = (x - mean) / scale
    design = np.column_stack((z, np.ones(z.shape[0])))
    weights = np.where(y == 1, y.size / (2.0 * positives), y.size / (2.0 * negatives))
    theta = np.zeros(design.shape[1], dtype=np.float64)
    for _ in range(steps):
        logits = np.clip(design @ theta, -40.0, 40.0)
        probs = 1.0 / (1.0 + np.exp(-logits))
        gradient = design.T @ ((probs - y) * weights) / y.size
        gradient[:-1] += regularization * theta[:-1]
        theta -= learning_rate * gradient
    return {
        "feature_mean": mean.tolist(),
        "feature_scale": scale.tolist(),
        "weights": theta[:-1].tolist(),
        "bias": float(theta[-1]),
        "threshold": 0.5,
        "training_examples": int(y.size),
        "normal_examples": negatives,
        "anomaly_examples": positives,
        "steps": steps,
        "learning_rate": learning_rate,
        "regularization": regularization,
    }


def positive_probability(features: np.ndarray, head: dict[str, Any]) -> np.ndarray:
    x = np.asarray(features, dtype=np.float64)
    standardized = (x - np.asarray(head["feature_mean"])) / np.asarray(head["feature_scale"])
    scores = standardized @ np.asarray(head["weights"]) + float(head["bias"])
    return 1.0 / (1.0 + np.exp(-np.clip(scores, -40.0, 40.0)))


class ResNet18LinearProbeDetector:
    """Frozen ImageNet ResNet-18 logits with a clip-trained binary logistic head."""

    def __init__(self, model_path: str | Path, head_path: str | Path):
        self.encoder = ResNet18ImageNetEncoder(model_path)
        self.head = json.loads(Path(head_path).read_text(encoding="utf-8"))
        self.threshold = float(self.head.get("threshold", 0.5))

    def __call__(self, frame: Any, index: int) -> tuple[bool, float]:
        probability = float(positive_probability(self.encoder.logits(frame)[None, :], self.head)[0])
        return probability >= self.threshold, probability
