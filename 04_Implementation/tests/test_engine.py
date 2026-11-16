import csv
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from sage.engine import (
    POLICIES,
    Event,
    ExperimentConfig,
    SimulationConfig,
    _select_frames,
    _event_metrics,
    run_experiment,
    simulate_sensor_cues,
    write_event_results,
    write_results,
    write_trace,
)


def toy_frames(count=40):
    frames = []
    for index in range(count):
        frame = np.zeros((96, 128, 3), dtype=np.uint8)
        if 10 <= index < 20:
            cv2.rectangle(frame, (index * 2, 30), (index * 2 + 14, 60), (255, 255, 255), -1)
        frames.append(frame)
    return frames


class EngineTests(unittest.TestCase):
    def test_event_metrics_match_intervals_and_report_misses(self):
        metrics = _event_metrics(
            [Event(0.0, 1.0), Event(2.0, 3.0), Event(6.0, 7.0)],
            [0.5, 1.5, 2.1],
            10.0,
        )
        self.assertEqual(metrics["events_detected"], 2)
        self.assertAlmostEqual(metrics["event_recall"], 2 / 3)
        self.assertEqual(metrics["missed_events"], 1)
        self.assertEqual(metrics["false_alarms"], 1)
        self.assertAlmostEqual(metrics["false_alarms_per_minute"], 6.0)
        self.assertAlmostEqual(metrics["mean_detection_latency_s"], 0.3)

    def test_sensor_simulation_repeats_for_seed(self):
        events = [Event(1.0, 2.0), Event(4.0, 5.0)]
        config = SimulationConfig(0.8, 10.0, 0.2, 31)
        self.assertEqual(simulate_sensor_cues(events, 10.0, config),
                         simulate_sensor_cues(events, 10.0, config))

    def test_budget_aware_enforces_quota_and_uses_shared_inputs(self):
        frames = toy_frames()
        config = ExperimentConfig(
            policies=("budget_aware",), budget_fraction=0.25,
            simulation=SimulationConfig(1.0, 0.0, 0.0, 9), warmup_frames=0,
        )
        scores = [0.0] * len(frames)
        selected = _select_frames("budget_aware", len(frames), 10.0, config, [1.0], scores)
        self.assertLessEqual(len(selected), 10)
        self.assertTrue(all(0 <= item < len(frames) for item in selected))

    def test_four_policies_emit_metrics_and_auditable_trace(self):
        frames = toy_frames()
        trace = []
        rows = run_experiment(
            frames, 10.0, [Event(1.0, 2.0, "moving_object")],
            ExperimentConfig(warmup_frames=0, simulation=SimulationConfig(seed=4)),
            "fixture", trace, "synthetic_test",
        )
        self.assertEqual({row["policy"] for row in rows}, set(POLICIES))
        self.assertTrue(all("event_recall" in row and "missed_events" in row for row in rows))
        self.assertEqual(len(trace), len(frames) * len(POLICIES))
        budget = next(row for row in rows if row["policy"] == "budget_aware")
        self.assertLessEqual(budget["frames_analyzed"], 10)
        for row in rows:
            if row["policy"] in {"video_adaptive", "budget_aware"}:
                self.assertGreaterEqual(row["processing_time_seconds"], row["scout_runtime_seconds"])
                self.assertEqual(row["scout_frames"], len(frames))

    def test_result_and_trace_exports(self):
        rows = [{"policy": "fixed_rate", "event_recall": 1.0}]
        trace = [{"policy": "fixed_rate", "frame_idx": 0, "selected": True}]
        with tempfile.TemporaryDirectory() as temp:
            result_csv, result_jsonl = write_results(rows, temp)
            trace_csv, trace_jsonl = write_trace(trace, temp)
            self.assertTrue(result_jsonl.exists())
            self.assertTrue(trace_jsonl.exists())
            with result_csv.open(newline="", encoding="utf-8") as stream:
                self.assertEqual(next(csv.DictReader(stream))["policy"], "fixed_rate")
            with trace_csv.open(newline="", encoding="utf-8") as stream:
                self.assertEqual(next(csv.DictReader(stream))["frame_idx"], "0")

    def test_per_event_rows_keep_types_and_count_misses(self):
        event_rows = []
        frames = [np.zeros((96, 128, 3), dtype=np.uint8) for _ in range(40)]
        events = [Event(1.0, 1.5, "conveyor_jam"), Event(2.0, 2.5, "worker_entry")]
        run_experiment(
            frames, 10.0, events,
            ExperimentConfig(policies=("fixed_rate",), warmup_frames=3),
            "typed_fixture", event_rows=event_rows,
        )
        self.assertEqual([row["event_type"] for row in event_rows], ["conveyor_jam", "worker_entry"])
        self.assertTrue(all(row["data_source"] == "user_provided" for row in event_rows))
        self.assertEqual(sum(row["missed"] for row in event_rows), 2)
        self.assertTrue(all(row["detected"] is False for row in event_rows))
        self.assertTrue(all(row["first_detection_time_s"] is None for row in event_rows))
        with tempfile.TemporaryDirectory() as temp:
            event_csv, event_jsonl = write_event_results(event_rows, temp)
            self.assertTrue(event_jsonl.exists())
            with event_csv.open(newline="", encoding="utf-8") as stream:
                exported = list(csv.DictReader(stream))
            self.assertEqual(exported[1]["event_type"], "worker_entry")
            self.assertEqual(exported[0]["missed"], "True")

    def test_pretrained_hog_model_loads_and_returns_a_score(self):
        from sage.engine import _HogPeopleDetector

        detected, score = _HogPeopleDetector()(toy_frames(1)[0], 0)
        self.assertIsInstance(detected, bool)
        self.assertIsInstance(score, float)


if __name__ == "__main__":
    unittest.main()
