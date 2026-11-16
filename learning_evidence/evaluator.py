from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from learning_evidence.programs.contract import ContractError, Decision, DomainRecord, records_from_fixture, stable_hash
from learning_evidence.warehouse.cohort_store import Repository
from learning_evidence.rollout.scale_gates import STATES, advance_for_outcome, decide
from learning_evidence.publication.scorecard import export_bundle, verify_bundle
from learning_evidence.learning_metrics.bias_adjustment import derive_context, derive_school_context
from learning_evidence.rollout.scale_reviews import ScaleReviews


class Application:
    def __init__(self, database: str | Path, context: Mapping[str, Any] | None = None):
        self.repository = Repository(database)
        self.scale_reviews = ScaleReviews(self.repository)
        self.context = dict(context or {})

    def ingest(self, record: DomainRecord) -> DomainRecord:
        current = self.repository.get_record(record.record_id)
        if current is None:
            self.repository.save_record(record)
            return record
        # 幂等以评分证据为准：同一份 payload 重放（包括新比较、中断恢复或输入重排）
        # 不推进版本，也不覆盖已经推进的工作流状态。
        if current.payload == record.payload:
            return current
        replacement = DomainRecord(record.record_id, record.payload, current.state,
                                   current.version + 1, record.occurred_at, record.source)
        self.repository.save_record(replacement, expected_version=current.version)
        return replacement

    def _comparison_record(self, record: DomainRecord) -> DomainRecord:
        """批次评分使用本批提交的证据内容及其首次入库的版本。

        工作流推进会在同一内容上继续推进版本；比较证据的版本应取该内容首次
        入库的版本，这样中断恢复后重算仍能得到同一份可复核的评分卡。
        历史更正会以新内容入库，评分卡随之记录更正后的版本。
        """
        version = self.repository.evidence_version(record.record_id, record.payload)
        if version is None:
            raise ContractError("comparison evidence was not stored")
        return DomainRecord(record.record_id, record.payload, record.state, version,
                            record.occurred_at, record.source)

    def _comparison_context(self, record: DomainRecord, population: list[DomainRecord]) -> dict[str, Any]:
        """单校上下文 = 本批次共用的群体证据 + 只依赖该校自身的权重。"""
        context = dict(self.context)
        context.update(derive_context(population))
        context.update(derive_school_context(record))
        return context

    def _apply_outcome(self, record: DomainRecord, decision: Decision) -> DomainRecord:
        """把决策结果落地到已存记录。

        只允许沿生命周期向前落地，重复恢复或重新比较不会把已发布结论推回去，
        也不会重复推进版本。
        """
        current = self.repository.get_record(record.record_id) or record
        target = advance_for_outcome(record, decision)
        if current.state == target.state and current.payload == target.payload:
            return current
        if STATES.index(target.state) <= STATES.index(current.state):
            return current
        advanced = DomainRecord(current.record_id, target.payload, target.state,
                                current.version + 1, current.occurred_at, current.source)
        self.repository.save_record(advanced, expected_version=current.version)
        return advanced

    def process(self, record: DomainRecord, population: list[DomainRecord] | None = None) -> tuple[DomainRecord, Decision]:
        """单校追踪。未显式给出比较人口时，该校自成一个比较人口。

        单校结论基于该校当前已存状态，沿用原有追踪口径；批次评分则使用该批次
        规范化后的输入，避免历史批次状态影响同一输入的可复核结果。
        """
        inputs = sorted(population or [record], key=lambda item: item.record_id)
        stored = self.ingest(record)
        context = self._comparison_context(stored, inputs)
        decision = decide(stored, context)
        population_evidence = derive_context(inputs)
        decision = decision.with_population(population_evidence["population_hash"],
                                            population_evidence["population_size"])
        self.repository.save_decision(decision)
        advanced = self._apply_outcome(stored, decision)
        return advanced, decision

    def run_fixture(self, fixture: Mapping[str, Any], output: str | Path) -> dict[str, Any]:
        records = records_from_fixture(fixture)
        fixture_hash = stable_hash(fixture)
        run_id = self.repository.begin_run(fixture_hash, len(records))
        completed = self.repository.completed_run(run_id)
        if completed is not None:
            return completed
        # 比较人口按学校标识规范化，人员顺序不影响群体证据、评分或推进判断。
        population = sorted(records, key=lambda item: item.record_id)
        # 先把整批学校摄入，再一次性固定人口证据：评分不依赖导入顺序、
        # 也不受库内旧批次残留记录影响。历史更正会在库内推进版本，评分卡记录
        # 的版本也随之反映更正后的证据。
        for record in population:
            self.ingest(record)
        population = [self._comparison_record(record) for record in population]
        population_evidence = derive_context(population)
        decisions: dict[str, Decision] = {}
        final_records: list[DomainRecord] = []
        for record in population:
            context = self._comparison_context(record, population)
            decision = decide(record, context).with_population(
                population_evidence["population_hash"], population_evidence["population_size"])
            self.repository.save_decision(decision)
            decisions[record.record_id] = decision
            final_records.append(self._apply_outcome(record, decision))
        snapshot = self.repository.snapshot()
        if snapshot["chain_errors"]:
            raise ContractError("audit chain verification failed")
        manifest = export_bundle(output, final_records, decisions, snapshot, self.repository.event_rows())
        card = self.repository.publish_cohort_card(run_id, str(fixture.get("scenario") or "current cohort"),
                                                   [record.record_id for record in population], decisions,
                                                   records=population)
        result = {"run_id": run_id, "fixture_hash": fixture_hash, "records": len(final_records),
                  "decisions": len(decisions), "manifest": manifest, "snapshot": snapshot,
                  "cohort_card": card}
        self.repository.finish_run(run_id, result)
        return result

    def inspect(self) -> dict[str, Any]:
        return {"snapshot": self.repository.snapshot(), "records": [record.__dict__ for record in self.repository.list_records()],
                "decisions": self.repository.decision_rows()}


def load_fixture(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read fixture: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("fixture root must be an object")
    return value


def run(fixture_path: str | Path, database: str | Path, output: str | Path,
        context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return Application(database, context).run_fixture(load_fixture(fixture_path), output)


def verify(database: str | Path, output: str | Path) -> dict[str, Any]:
    repository = Repository(database)
    chain_errors = repository.verify_chain()
    bundle_errors = verify_bundle(output)
    return {"ok": not chain_errors and not bundle_errors, "chain_errors": chain_errors,
            "bundle_errors": bundle_errors, "snapshot": repository.snapshot()}
