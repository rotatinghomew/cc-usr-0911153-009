import unittest

from learning_evidence.programs.contract import DomainRecord
from learning_evidence.learning_metrics.bias_adjustment import equity_summary


class CohortDenominatorTests(unittest.TestCase):
    def test_school_split_does_not_change_language_gap(self):
        def school(identifier, language, learners, outcome):
            return DomainRecord(identifier, {
                "school_code": identifier, "language_group": language,
                "learner_count": learners, "baseline_score": 0,
                "outcome_score": outcome, "teacher_support": 0,
                "missing_rate": 0, "consent_rate": 1,
                "connectivity": 1, "usage_minutes": 6000,
            }, "registered")

        large = school("large", "a", 1000, 1.0)
        small = school("small", "a", 1, 0.0)
        comparison = school("comparison", "b", 1000, 0.4)
        before = equity_summary([large, small, comparison])
        after = equity_summary([
            school("north", "a", 500, 1.0),
            school("south", "a", 500, 1.0),
            small, comparison,
        ])
        self.assertEqual(before["gap"], after["gap"])


if __name__ == "__main__":
    unittest.main()
