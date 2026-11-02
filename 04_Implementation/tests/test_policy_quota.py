import unittest

from sage.engine import ExperimentConfig, POLICIES, _select_frames


class MatchedQuotaTest(unittest.TestCase):
    def test_all_policies_select_same_exact_budget_quota(self):
        frame_count = 25
        fps = 5.0
        config = ExperimentConfig(budget_fraction=0.25, sensor_window_s=0.8)
        cues = [0.4, 2.0]
        scout = [0.0] * frame_count
        scout[6:10] = [0.2] * 4
        scout[16:19] = [0.3] * 3
        expected = 7  # ceil(25 * 0.25)

        selections = {
            policy: _select_frames(policy, frame_count, fps, config, cues, scout)
            for policy in POLICIES
        }

        self.assertTrue(all(len(indices) == expected for indices in selections.values()))
        self.assertTrue(all(indices == sorted(set(indices)) for indices in selections.values()))
        self.assertTrue(all(indices == _select_frames(policy, frame_count, fps, config, cues, scout)
                            for policy, indices in selections.items()))
