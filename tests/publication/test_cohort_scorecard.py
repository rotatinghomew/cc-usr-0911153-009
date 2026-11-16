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

    def _stored_decisions(self, card):
        """取回属于该评分卡比较人口的决策对象。"""
        from learning_evidence.programs.contract import Decision, RuleResult
        stored = {}
        with self.application.repository.connect() as connection:
            rows = connection.execute("SELECT record_id, decision_json FROM decisions").fetchall()
        for row in rows:
            body = json.loads(row["decision_json"])
            if body.get("population_hash") != card["population_hash"]:
                continue
            stored[row["record_id"]] = Decision(
                body["record_id"], body["outcome"], body["score"], tuple(body["reasons"]),
                tuple(RuleResult(item["code"], item["passed"], item["score"], item["severity"],
                                 item["message"], item["evidence"]) for item in body["rules"]),
                body["metrics"], body["decided_at"],
                body.get("population_hash", ""), body.get("population_size", 0))
        return stored

    def test_import_order_does_not_change_scores_or_candidates(self):
        baseline = self.application.run_fixture(self.fixture, self.root / "baseline")
        for label, order in (("reversed", list(reversed(range(len(self.fixture["records"]))))),
                             ("interleaved", [3, 0, 7, 1, 6, 2, 5, 4])):
            candidate = dict(self.fixture, records=[self.fixture["records"][index] for index in order])
            with tempfile.TemporaryDirectory() as directory:
                result = Application(Path(directory) / "db").run_fixture(candidate, Path(directory) / "out")
            self.assertEqual(result["cohort_card"]["evidence_hash"], baseline["cohort_card"]["evidence_hash"], label)
            self.assertEqual(result["cohort_card"]["population_hash"], baseline["cohort_card"]["population_hash"])
            self.assertEqual({row["school_id"]: (row["score"], row["outcome"]) for row in result["cohort_card"]["schools"]},
                             {row["school_id"]: (row["score"], row["outcome"]) for row in baseline["cohort_card"]["schools"]})

    def test_every_school_is_scored_against_the_same_population_evidence(self):
        result = self.application.run_fixture(self.fixture, self.root / "output")
        card = result["cohort_card"]
        decisions = self._stored_decisions(card)
        from learning_evidence.learning_metrics.bias_adjustment import derive_context
        from learning_evidence.programs.contract import records_from_fixture
        expected = derive_context(records_from_fixture(self.fixture))
        self.assertEqual({decision.population_hash for decision in decisions.values()}, {expected["population_hash"]})
        self.assertEqual({decision.population_size for decision in decisions.values()}, {len(self.fixture["records"])})
        self.assertEqual(card["population_hash"], expected["population_hash"])

    def test_mixing_schools_from_two_populations_is_rejected(self):
        first = self.application.run_fixture(self.fixture, self.root / "first")
        late = dict(self.fixture["records"][0], record_id="learning_program-009")
        second_fixture = dict(self.fixture, records=self.fixture["records"] + [late])
        second = self.application.run_fixture(second_fixture, self.root / "second")
        self.assertNotEqual(first["cohort_card"]["population_hash"], second["cohort_card"]["population_hash"])
        decisions = self._stored_decisions(second["cohort_card"])
        # 只重算晚到学校而沿用旧口径的其余学校：必须被拒绝，不能并列呈现。
        old_decisions = self._stored_decisions(first["cohort_card"])
        mixed = dict(decisions)
        for school_id, decision in old_decisions.items():
            mixed[school_id] = decision
        ids = [row["school_id"] for row in second["cohort_card"]["schools"]]
        with self.assertRaisesRegex(ContractError, "mixes comparison populations"):
            self.application.repository.publish_cohort_card("mixed", "cohort", ids, mixed)
        self.assertEqual(self.application.repository.cohort_card(first["run_id"]), first["cohort_card"])

    def test_resumed_comparison_republishes_the_same_evidence(self):
        complete = self.application.run_fixture(self.fixture, self.root / "complete")
        from learning_evidence.programs.contract import records_from_fixture, stable_hash
        from learning_evidence.learning_metrics.bias_adjustment import derive_context
        from learning_evidence.rollout.scale_gates import decide
        interrupted = Application(self.root / "resumed")
        population = sorted(records_from_fixture(self.fixture), key=lambda item: item.record_id)
        run_id = interrupted.repository.begin_run(stable_hash(self.fixture), len(population))
        evidence = derive_context(population)
        for record in population[:4]:
            interrupted.ingest(record)
            decision = decide(record, interrupted._comparison_context(record, population)).with_population(
                evidence["population_hash"], evidence["population_size"])
            interrupted.repository.save_decision(decision)
            interrupted._apply_outcome(record, decision)
        # 中途退出的批次重新开始时不得只重算剩余学校或混用新旧口径。
        resumed = interrupted.run_fixture(self.fixture, self.root / "resumed-output")
        self.assertEqual(resumed["run_id"], run_id)
        self.assertEqual(resumed["cohort_card"]["evidence_hash"], complete["cohort_card"]["evidence_hash"])
        self.assertEqual(resumed["cohort_card"]["schools"], complete["cohort_card"]["schools"])
        self.assertEqual({row["school_id"] for row in resumed["cohort_card"]["schools"]},
                         {row["record_id"] for row in self.fixture["records"]})

    def test_published_card_rejects_tampered_evidence(self):
        result = self.application.run_fixture(self.fixture, self.root / "output")
        with self.application.repository.connect() as connection:
            connection.execute("UPDATE cohort_scorecards SET school_results_json=? WHERE card_id=?",
                               (json.dumps([{"school_id": "forged"}]), result["run_id"]))
        with self.assertRaisesRegex(ContractError, "evidence is inconsistent"):
            self.application.repository.cohort_card(result["run_id"])

    def test_single_school_tracking_stays_auditable(self):
        from learning_evidence.programs.contract import DomainRecord
        payload = self.fixture["records"][0]["payload"]
        final, decision = self.application.process(DomainRecord("learning_program-001", payload))
        self.assertEqual(decision.population_size, 1)
        self.assertTrue(decision.population_hash)
        stored = self.application.repository.get_record("learning_program-001")
        self.assertEqual(stored.state, final.state)
        self.assertEqual([row["record_id"] for row in self.application.inspect()["decisions"]],
                         ["learning_program-001"])
