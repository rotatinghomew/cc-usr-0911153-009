from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from learning_evidence.evaluator import Application
from learning_evidence.programs.contract import ContractError


FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "acceptance.json"


class CohortScorecardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.application = Application(self.root / "cohort.sqlite3")
        self.fixture = json.loads(FIXTURE.read_text())

    def test_published_card_has_all_decisions_and_survives_restart(self):
        result = self.application.run_fixture(self.fixture, self.root / "output")
        card = result["cohort_card"]
        self.assertEqual(card["school_count"], len(self.fixture["records"]))
        self.assertEqual({row["school_id"] for row in card["schools"]},
                         {row["record_id"] for row in self.fixture["records"]})
        reopened = Application(self.root / "cohort.sqlite3")
        self.assertEqual(reopened.repository.cohort_card(result["run_id"]), card)
        self.assertEqual(reopened.run_fixture(self.fixture, self.root / "output")["cohort_card"], card)

    def test_changed_population_cannot_overwrite_published_card(self):
        result = self.application.run_fixture(self.fixture, self.root / "output")
        original = result["cohort_card"]
        altered = dict(self.fixture, records=list(reversed(self.fixture["records"])))
        second = self.application.run_fixture(altered, self.root / "second")
        self.assertNotEqual(result["run_id"], second["run_id"])
        self.assertEqual(self.application.repository.cohort_card(result["run_id"]), original)
        with self.assertRaisesRegex(ContractError, "cannot be silently overwritten"):
            self.application.repository.publish_cohort_card(
                result["run_id"], original["cohort_label"],
                [row["school_id"] for row in original["schools"]],
                {row["school_id"]: self._different_decision(row) for row in original["schools"]})

    def _different_decision(self, row):
        from learning_evidence.programs.contract import Decision
        return Decision(row["school_id"], "review", 0.0, ("new",), (), {})
