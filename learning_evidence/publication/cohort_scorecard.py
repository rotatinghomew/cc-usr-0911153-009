from __future__ import annotations

import json
import sqlite3
from typing import Any, Mapping

from learning_evidence.programs.contract import ContractError, Decision, DomainRecord, canonical_json, stable_hash, utc_now
from learning_evidence.learning_metrics.bias_adjustment import population_hash as comparison_population_hash


def prepare_scorecards(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS cohort_scorecards(
        card_id TEXT PRIMARY KEY, cohort_label TEXT NOT NULL, population_hash TEXT NOT NULL,
        evidence_hash TEXT NOT NULL, school_count INTEGER NOT NULL,
        school_results_json TEXT NOT NULL, created_at TEXT NOT NULL
    )""")


def evidence_fingerprint(schools: list[Mapping[str, Any]]) -> str:
    return stable_hash(schools)


def assemble_card(cohort_label: str, records: list[DomainRecord], decisions: Mapping[str, Decision]) -> dict[str, Any]:
    if not cohort_label.strip() or not records or len({record.record_id for record in records}) != len(records):
        raise ContractError("scorecard requires a named cohort with unique schools")
    if set(decisions) != {record.record_id for record in records}:
        raise ContractError("scorecard decisions must cover exactly the compared schools")
    # 同一评分卡只能基于同一份比较人口：任何一所学校沿用旧批次口径都会被拒绝，
    # 而不是把新旧结果并列呈现。
    expected_population = comparison_population_hash(records)
    partial = [decision for decision in decisions.values() if decision.population_hash]
    if partial and len(partial) != len(decisions):
        raise ContractError("scorecard mixes comparison populations")
    results = []
    for record in sorted(records, key=lambda item: item.record_id):
        decision = decisions[record.record_id]
        if decision.record_id != record.record_id:
            raise ContractError("scorecard decision belongs to another school")
        if decision.population_hash and decision.population_hash != expected_population:
            raise ContractError("scorecard mixes comparison populations")
        if decision.population_size and decision.population_size != len(records):
            raise ContractError("scorecard mixes comparison populations")
        results.append({"school_id": record.record_id, "record_version": record.version,
                        "record_fingerprint": record.content_fingerprint,
                        "decision_fingerprint": decision.fingerprint, "score": decision.score,
                        "outcome": decision.outcome})
    return {"cohort_label": cohort_label, "population_hash": expected_population,
            "evidence_hash": evidence_fingerprint(results), "school_count": len(results),
            "schools": results}


def publish_card(connection: sqlite3.Connection, card_id: str, cohort_label: str,
                 records: list[DomainRecord], decisions: Mapping[str, Decision]) -> dict[str, Any]:
    prepare_scorecards(connection)
    card = assemble_card(cohort_label, records, decisions)
    row = connection.execute("SELECT evidence_hash FROM cohort_scorecards WHERE card_id=?", (card_id,)).fetchone()
    if row:
        if row[0] != card["evidence_hash"]:
            raise ContractError("published scorecard cannot be silently overwritten")
        return read_card(connection, card_id)
    connection.execute("INSERT INTO cohort_scorecards VALUES(?,?,?,?,?,?,?)",
                       (card_id, cohort_label, card["population_hash"], card["evidence_hash"],
                        card["school_count"], canonical_json(card["schools"]), utc_now()))
    return read_card(connection, card_id)


def read_card(connection: sqlite3.Connection, card_id: str) -> dict[str, Any]:
    prepare_scorecards(connection)
    row = connection.execute("SELECT * FROM cohort_scorecards WHERE card_id=?", (card_id,)).fetchone()
    if row is None:
        raise ContractError("unknown cohort scorecard")
    schools = json.loads(row["school_results_json"])
    # 已发布评分卡必须自洽：证据指纹要能由卡内学校结果重新算出，
    # 否则扩容评议不能声称自己复用了这张卡的证据。
    if evidence_fingerprint(schools) != row["evidence_hash"]:
        raise ContractError("published scorecard evidence is inconsistent")
    return {"card_id": card_id, "cohort_label": row["cohort_label"],
            "population_hash": row["population_hash"], "evidence_hash": row["evidence_hash"],
            "school_count": row["school_count"], "schools": schools,
            "created_at": row["created_at"]}
