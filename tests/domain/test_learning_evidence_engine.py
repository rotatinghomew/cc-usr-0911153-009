from __future__ import annotations

import unittest
from learning_evidence.programs.contract import DomainRecord
from learning_evidence.evaluation.bias_adjustment import adjusted_effect, equity_summary, observed_gain, persistence


class BiasAdjustmentTests(unittest.TestCase):
    def record(self, key, language="a", outcome=75):
        return DomainRecord(key, {"school_code": key, "grade_band": "g5", "subject": "math", "learner_count": 100,
            "usage_minutes": 1200, "baseline_score": 60, "outcome_score": outcome, "missing_rate": .05,
            "teacher_support": .4, "connectivity": .9, "language_group": language, "consent_rate": .95})

    def test_adjustment_shrinks_observed_gain(self):
        record = self.record("a")
        self.assertGreater(observed_gain(record), adjusted_effect(record)["adjusted"])

    def test_equity_and_persistence(self):
        rows = [self.record("a", "x", 80), self.record("b", "y", 65)]
        self.assertGreater(equity_summary(rows)["gap"], 0.0)
        self.assertTrue(0.0 <= persistence(rows)["stability"] <= 1.0)
