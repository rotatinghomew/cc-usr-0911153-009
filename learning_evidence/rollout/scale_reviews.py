"""使用已发布评分卡安排学校扩容评议及名额确认。"""
import math

from learning_evidence.programs.contract import ContractError


class ScaleReviews:
    def __init__(self, repository):
        self.repository = repository
        with repository.connect() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS scale_campaigns(
                    campaign_id TEXT PRIMARY KEY, card_id TEXT NOT NULL,
                    evidence_hash TEXT NOT NULL, minimum_score REAL NOT NULL,
                    seats INTEGER NOT NULL CHECK(seats>=0));
                CREATE TABLE IF NOT EXISTS school_scale_reviews(
                    campaign_id TEXT NOT NULL, school_id TEXT NOT NULL,
                    score REAL NOT NULL, source_outcome TEXT NOT NULL, status TEXT NOT NULL,
                    seats INTEGER NOT NULL DEFAULT 0, reason TEXT NOT NULL DEFAULT '',
                    PRIMARY KEY(campaign_id,school_id));
            """)

    def open(self, campaign_id, card_id, minimum_score, seats):
        if not campaign_id or type(seats) is not int or seats < 0:
            raise ContractError("扩容评议及名额无效")
        if isinstance(minimum_score, bool) or not isinstance(minimum_score, (int, float)) or not math.isfinite(minimum_score) or not 0 <= minimum_score <= 1:
            raise ContractError("候选评分门槛无效")
        with self.repository.transaction() as c:
            from learning_evidence.publication.cohort_scorecard import read_card
            card = read_card(c, card_id)
            old = c.execute("SELECT * FROM scale_campaigns WHERE campaign_id=?", (campaign_id,)).fetchone()
            if old:
                if (old["card_id"], old["minimum_score"], old["seats"]) != (card_id, minimum_score, seats):
                    raise ContractError("同一扩容评议不可混用评分卡或门槛")
                return self._read(c, campaign_id)
            c.execute("INSERT INTO scale_campaigns VALUES(?,?,?,?,?)",
                      (campaign_id, card_id, card["evidence_hash"], minimum_score, seats))
            for school in card["schools"]:
                status = "pending" if school["score"] >= minimum_score else "insufficient"
                c.execute("INSERT INTO school_scale_reviews(campaign_id,school_id,score,source_outcome,status) VALUES(?,?,?,?,?)",
                          (campaign_id, school["school_id"], school["score"], school["outcome"], status))
            return self._read(c, campaign_id)

    def decide(self, campaign_id, school_id, status, reason, seats=0):
        if status not in {"approved", "deferred"} or not isinstance(reason, str) or not reason.strip():
            raise ContractError("评议需要明确结论及依据")
        if type(seats) is not int or seats < 0 or (status == "deferred" and seats != 0):
            raise ContractError("名额无效")
        with self.repository.transaction() as c:
            campaign = c.execute("SELECT * FROM scale_campaigns WHERE campaign_id=?", (campaign_id,)).fetchone()
            row = c.execute("SELECT * FROM school_scale_reviews WHERE campaign_id=? AND school_id=?",
                            (campaign_id, school_id)).fetchone()
            if campaign is None or row is None:
                raise ContractError("学校不属于本次比较人口")
            if row["status"] != "pending":
                if (row["status"], row["reason"], row["seats"]) == (status, reason, seats):
                    return
                raise ContractError("评分不足或评议已完成，不可覆盖历史")
            if status == "approved":
                if row["source_outcome"] in {"hold", "reject"} or seats == 0:
                    raise ContractError("既有安全门禁未放行或未申请扩容名额")
                allocated = c.execute("SELECT COALESCE(SUM(seats),0) FROM school_scale_reviews WHERE campaign_id=?",
                                      (campaign_id,)).fetchone()[0]
                if allocated + seats > campaign["seats"]:
                    raise ContractError("本轮扩容名额不足")
            c.execute("UPDATE school_scale_reviews SET status=?,seats=?,reason=? WHERE campaign_id=? AND school_id=?",
                      (status, seats, reason, campaign_id, school_id))

    def _read(self, c, campaign_id):
        campaign = c.execute("SELECT * FROM scale_campaigns WHERE campaign_id=?", (campaign_id,)).fetchone()
        if campaign is None:
            raise ContractError("扩容评议不存在")
        return dict(campaign) | {"schools": [dict(r) for r in c.execute(
            "SELECT * FROM school_scale_reviews WHERE campaign_id=? ORDER BY score DESC,school_id", (campaign_id,))]}

    def inspect(self, campaign_id):
        with self.repository.connect() as c:
            return self._read(c, campaign_id)
