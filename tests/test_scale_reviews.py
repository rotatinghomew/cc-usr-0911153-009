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
