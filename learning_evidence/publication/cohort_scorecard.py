from __future__ import annotations

import json
import sqlite3
from typing import Any, Mapping

from learning_evidence.programs.contract import ContractError, Decision, DomainRecord, canonical_json, stable_hash, utc_now


def prepare_scorecards(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS cohort_scorecards(
        card_id TEXT PRIMARY KEY, cohort_label TEXT NOT NULL, population_hash TEXT NOT NULL,
        evidence_hash TEXT NOT NULL, school_count INTEGER NOT NULL,
        school_results_json TEXT NOT NULL, created_at TEXT NOT NULL
    )""")


def assemble_card(cohort_label: str, records: list[DomainRecord], decisions: Mapping[str, Decision]) -> dict[str, Any]:
    if not cohort_label.strip() or not records or len({record.record_id for record in records}) != len(records):
        raise ContractError("scorecard requires a named cohort with unique schools")
    if set(decisions) != {record.record_id for record in records}:
        raise ContractError("scorecard decisions must cover exactly the compared schools")
    results = []
    for record in sorted(records, key=lambda item: item.record_id):
        decision = decisions[record.record_id]
        if decision.record_id != record.record_id:
            raise ContractError("scorecard decision belongs to another school")
        results.append({"school_id": record.record_id, "record_version": record.version,
                        "record_fingerprint": record.fingerprint,
                        "decision_fingerprint": decision.fingerprint, "score": decision.score,
                        "outcome": decision.outcome})
    return {"cohort_label": cohort_label, "population_hash": stable_hash([
        [item["school_id"], item["record_version"], item["record_fingerprint"]] for item in results]),
        "evidence_hash": stable_hash(results), "school_count": len(results), "schools": results}


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
    return {"card_id": card_id, "cohort_label": row["cohort_label"],
            "population_hash": row["population_hash"], "evidence_hash": row["evidence_hash"],
            "school_count": row["school_count"], "schools": json.loads(row["school_results_json"]),
            "created_at": row["created_at"]}
