from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Iterable

from learning_evidence.programs.contract import DomainRecord, bounded, finite_number, normalized_text, stable_hash


def observed_gain(record: DomainRecord) -> float:
    baseline = finite_number(record.payload.get("baseline_score", 0.0))
    outcome = finite_number(record.payload.get("outcome_score", 0.0))
    scale = max(1.0, abs(baseline), abs(outcome))
    return (outcome - baseline) / scale


def reliability_weight(record: DomainRecord) -> float:
    missing = bounded(finite_number(record.payload.get("missing_rate", 0.0)))
    consent = bounded(finite_number(record.payload.get("consent_rate", 0.0)))
    connectivity = bounded(finite_number(record.payload.get("connectivity", 0.0)))
    usage = bounded(finite_number(record.payload.get("usage_minutes", 0.0)) / 6000.0)
    return bounded((1.0 - missing) * 0.35 + consent * 0.25 + connectivity * 0.20 + usage * 0.20)


def adjusted_effect(record: DomainRecord) -> dict[str, float]:
    gain = observed_gain(record)
    reliability = reliability_weight(record)
    teacher = bounded(finite_number(record.payload.get("teacher_support", 0.0)))
    shrinkage = 0.35 + reliability * 0.65
    adjusted = gain * shrinkage - teacher * 0.04
    return {"observed": gain, "reliability": reliability, "adjusted": adjusted,
            "lower": adjusted - (1.0 - reliability) * 0.12, "upper": adjusted + (1.0 - reliability) * 0.12}


def equity_summary(records: Iterable[DomainRecord]) -> dict[str, float]:
    groups: dict[str, list[float]] = defaultdict(list)
    for record in records:
        key = normalized_text(record.payload.get("language_group", "unknown"))
        groups[key].append(adjusted_effect(record)["adjusted"])
    means = {key: statistics.fmean(values) for key, values in groups.items()}
    gap = max(means.values()) - min(means.values()) if means else 0.0
    return {"group_count": float(len(means)), "gap": gap, "fairness": bounded(1.0 - abs(gap))}


def persistence(records: Iterable[DomainRecord]) -> dict[str, float]:
    rows = sorted(records, key=lambda row: normalized_text(row.payload.get("school_code", row.record_id)))
    effects = [adjusted_effect(row)["adjusted"] for row in rows]
    if not effects:
        return {"mean": 0.0, "dispersion": 0.0, "stability": 0.0}
    dispersion = statistics.pstdev(effects) if len(effects) > 1 else 0.0
    return {"mean": statistics.fmean(effects), "dispersion": dispersion, "stability": bounded(1.0 - dispersion)}


def population_hash(records: Iterable[DomainRecord]) -> str:
    """比较人口的证据指纹：只由学校身份与评分证据决定，与导入顺序无关。"""
    rows = sorted((record.record_id, record.content_fingerprint) for record in records)
    return stable_hash(rows)


def derive_context(records: Iterable[DomainRecord]) -> dict[str, Any]:
    """从固定的比较人口推导群体权重。

    群体权重必须由同一份人口证据一次性算出，再供该批次的每一所学校共用；
    逐校重新推导会让评分取决于导入顺序和旧批次残留记录。
    """
    rows = sorted(records, key=lambda row: row.record_id)
    if not rows:
        return {"population_hash": "", "population_size": 0}
    equity = equity_summary(rows)
    stable = persistence(rows)
    return {"population_hash": population_hash(rows), "population_size": len(rows),
            "equity_gap_weight": 0.8 + abs(equity["gap"]) * 0.7,
            "effect_persistence_weight": 0.6 + stable["stability"] * 0.5,
            "scale_readiness_weight": 0.6 + equity["fairness"] * stable["stability"] * 0.6}


def derive_school_context(record: DomainRecord) -> dict[str, float]:
    """单校权重只取决于该校自身证据，不与同批其他学校耦合。"""
    effect = adjusted_effect(record)
    return {"learning_gain_weight": 0.8 + bounded(effect["adjusted"] + 0.5) * 0.4,
            "attrition_bias_weight": 1.2 - effect["reliability"] * 0.4}
