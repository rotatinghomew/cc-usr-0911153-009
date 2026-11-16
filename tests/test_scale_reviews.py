import json
import tempfile
import unittest
from pathlib import Path
from learning_evidence.evaluator import Application
from learning_evidence.programs.contract import ContractError, DomainRecord, Decision


class ScaleReviewsTests(unittest.TestCase):
    def test_scorecard_controls_candidate_queue_and_cannot_be_replaced(self):
        with tempfile.TemporaryDirectory() as d:
            app = Application(Path(d) / "db")
            fixture = json.loads((Path(__file__).resolve().parents[1] / "fixtures/acceptance.json").read_text())
            result = app.run_fixture(fixture, Path(d) / "out")
            card_id = result["cohort_card"]["card_id"]
            queue = app.scale_reviews.open("round", card_id, .55, 10)
            expected = {s["school_id"] for s in result["cohort_card"]["schools"] if s["score"] >= .55}
            self.assertEqual({s["school_id"] for s in queue["schools"] if s["status"] == "pending"}, expected)
            self.assertEqual(Application(Path(d) / "db").scale_reviews.inspect("round"), queue)
            with self.assertRaises(ContractError):
                app.scale_reviews.open("round", card_id, .4, 10)
            school = next(s["school_id"] for s in queue["schools"] if s["status"] == "pending")
            with self.assertRaises(ContractError):
                app.scale_reviews.decide("round", school, "approved", "评议", 1)

    def test_confirmations_share_seats_and_preserve_completed_decisions(self):
        with tempfile.TemporaryDirectory() as d:
            app = Application(Path(d) / "db")
            decisions = {}
            for name in ("a", "b"):
                app.ingest(DomainRecord(name, {}))
                decisions[name] = Decision(name, "approve", .8, ("人工复核",), (), {})
                app.repository.save_decision(decisions[name])
            app.repository.publish_cohort_card("card", "cohort", ["a", "b"], decisions)
            app.scale_reviews.open("round", "card", .6, 1)
            app.scale_reviews.decide("round", "a", "approved", "证据及支持准备充分", 1)
            with self.assertRaises(ContractError):
                app.scale_reviews.decide("round", "b", "approved", "评议通过", 1)
            app.scale_reviews.decide("round", "b", "deferred", "等候后续名额")
            with self.assertRaises(ContractError):
                app.scale_reviews.decide("round", "a", "deferred", "改写旧结论")

    def test_reopening_review_requires_the_published_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            app = Application(Path(d) / "db")
            fixture = json.loads((Path(__file__).resolve().parents[1] / "fixtures/acceptance.json").read_text())
            result = app.run_fixture(fixture, Path(d) / "out")
            card_id = result["cohort_card"]["card_id"]
            queue = app.scale_reviews.open("round", card_id, .55, 10)
            # 中途退出后恢复：同一评分卡、同一人口证据，重开得到同一评议队列。
            self.assertEqual(Application(Path(d) / "db").scale_reviews.open("round", card_id, .55, 10), queue)
            with app.repository.connect() as c:
                c.execute("UPDATE cohort_scorecards SET evidence_hash='0'*64 WHERE card_id=?", (card_id,))
            with self.assertRaises(ContractError):
                app.scale_reviews.open("round", card_id, .55, 10)

    def test_late_school_gets_a_new_round_instead_of_mixing_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            app = Application(Path(d) / "db")
            fixture = json.loads((Path(__file__).resolve().parents[1] / "fixtures/acceptance.json").read_text())
            first = app.run_fixture(fixture, Path(d) / "first")
            late = dict(fixture["records"][0], record_id="learning_program-009")
            second = app.run_fixture(dict(fixture, records=fixture["records"] + [late]), Path(d) / "second")
            self.assertNotEqual(first["cohort_card"]["evidence_hash"], second["cohort_card"]["evidence_hash"])
            original = app.scale_reviews.open("round-1", first["cohort_card"]["card_id"], .55, 10)
            updated = app.scale_reviews.open("round-2", second["cohort_card"]["card_id"], .55, 10)
            self.assertEqual({s["school_id"] for s in original["schools"]},
                             {row["record_id"] for row in fixture["records"]})
            self.assertIn("learning_program-009", {s["school_id"] for s in updated["schools"]})
            # 旧评议保留原证据，复核时仍可核对，不被新口径替换。
            self.assertEqual(app.scale_reviews.inspect("round-1"), original)
