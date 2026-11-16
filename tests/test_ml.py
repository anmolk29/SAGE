import unittest

import numpy as np

from sage.engine import ExperimentConfig
from sage.ml import fit_linear_probe, positive_probability


class LinearProbeTests(unittest.TestCase):
    def test_probe_separates_simple_balanced_feature_fixture(self):
        features = np.asarray([
            [-2.0, -1.0], [-1.5, -1.0], [-1.0, -1.5],
            [1.0, 1.0], [1.5, 1.0], [2.0, 1.5],
        ])
        labels = np.asarray([0, 0, 0, 1, 1, 1])
        head = fit_linear_probe(features, labels)
        probabilities = positive_probability(features, head)
        self.assertTrue(np.all(probabilities[:3] < 0.5))
        self.assertTrue(np.all(probabilities[3:] >= 0.5))
        self.assertEqual(head["normal_examples"], 3)
        self.assertEqual(head["anomaly_examples"], 3)

    def test_resnet_detector_requires_both_weight_paths(self):
        with self.assertRaisesRegex(ValueError, "model_path and head_path"):
            ExperimentConfig(detector="resnet18_probe")


if __name__ == "__main__":
    unittest.main()
