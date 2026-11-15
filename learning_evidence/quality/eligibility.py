from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from learning_evidence.programs.contract import DomainRecord, RuleResult, bounded, finite_number, normalized_text

RuleFunction = Callable[[DomainRecord, Mapping[str, Any]], RuleResult]

def _number(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    if not text:
        return 0.0
    try:
        return finite_number(text)
    except ValueError:
        return float(sum(ord(ch) for ch in text) % 101)

def _context_number(context: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return finite_number(context.get(key, default))
    except ValueError:
        return default

def _result(code: str, value: float, threshold: float, higher_is_better: bool, message: str, evidence: dict[str, Any]) -> RuleResult:
    distance = (value - threshold) if higher_is_better else (threshold - value)
    passed = distance >= 0
    scale = max(1.0, abs(threshold))
    score = bounded(0.5 + distance / (2.0 * scale))
    severity = 'info' if passed else ('critical' if score < 0.2 else 'error')
    return RuleResult(code, passed, score, severity, message, evidence)

def check_school_code_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_school_code_presence_threshold', 10.333)
    return _result('check_school_code_presence', adjusted, threshold, True, 'validates school_code presence',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_school_code_range_threshold', 12.667)
    return _result('check_school_code_range', adjusted, threshold, True, 'validates school_code range',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_school_code_stability_threshold', 15.0)
    return _result('check_school_code_stability', adjusted, threshold, False, 'validates school_code stability',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_school_code_freshness_threshold', 17.333)
    return _result('check_school_code_freshness', adjusted, threshold, True, 'validates school_code freshness',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_school_code_coverage_threshold', 19.667)
    return _result('check_school_code_coverage', adjusted, threshold, True, 'validates school_code coverage',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_school_code_consistency_threshold', 22.0)
    return _result('check_school_code_consistency', adjusted, threshold, False, 'validates school_code consistency',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_school_code_risk_threshold', 24.333)
    return _result('check_school_code_risk', adjusted, threshold, True, 'validates school_code risk',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_school_code_confidence_threshold', 26.667)
    return _result('check_school_code_confidence', adjusted, threshold, True, 'validates school_code confidence',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_school_code_dependency_threshold', 29.0)
    return _result('check_school_code_dependency', adjusted, threshold, False, 'validates school_code dependency',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_school_code_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'school_code')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_school_code_readiness_threshold', 31.333)
    return _result('check_school_code_readiness', adjusted, threshold, True, 'validates school_code readiness',
                   {'field': 'school_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_grade_band_presence_threshold', 9.333)
    return _result('check_grade_band_presence', adjusted, threshold, True, 'validates grade_band presence',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_grade_band_range_threshold', 11.667)
    return _result('check_grade_band_range', adjusted, threshold, False, 'validates grade_band range',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_grade_band_stability_threshold', 14.0)
    return _result('check_grade_band_stability', adjusted, threshold, True, 'validates grade_band stability',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_grade_band_freshness_threshold', 16.333)
    return _result('check_grade_band_freshness', adjusted, threshold, True, 'validates grade_band freshness',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_grade_band_coverage_threshold', 18.667)
    return _result('check_grade_band_coverage', adjusted, threshold, False, 'validates grade_band coverage',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_grade_band_consistency_threshold', 21.0)
    return _result('check_grade_band_consistency', adjusted, threshold, True, 'validates grade_band consistency',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_grade_band_risk_threshold', 23.333)
    return _result('check_grade_band_risk', adjusted, threshold, True, 'validates grade_band risk',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_grade_band_confidence_threshold', 25.667)
    return _result('check_grade_band_confidence', adjusted, threshold, False, 'validates grade_band confidence',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_grade_band_dependency_threshold', 28.0)
    return _result('check_grade_band_dependency', adjusted, threshold, True, 'validates grade_band dependency',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grade_band_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grade_band')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_grade_band_readiness_threshold', 30.333)
    return _result('check_grade_band_readiness', adjusted, threshold, True, 'validates grade_band readiness',
                   {'field': 'grade_band', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_subject_presence_threshold', 8.333)
    return _result('check_subject_presence', adjusted, threshold, False, 'validates subject presence',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_subject_range_threshold', 10.667)
    return _result('check_subject_range', adjusted, threshold, True, 'validates subject range',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_subject_stability_threshold', 13.0)
    return _result('check_subject_stability', adjusted, threshold, True, 'validates subject stability',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_subject_freshness_threshold', 15.333)
    return _result('check_subject_freshness', adjusted, threshold, False, 'validates subject freshness',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_subject_coverage_threshold', 17.667)
    return _result('check_subject_coverage', adjusted, threshold, True, 'validates subject coverage',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_subject_consistency_threshold', 20.0)
    return _result('check_subject_consistency', adjusted, threshold, True, 'validates subject consistency',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_subject_risk_threshold', 22.333)
    return _result('check_subject_risk', adjusted, threshold, False, 'validates subject risk',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_subject_confidence_threshold', 24.667)
    return _result('check_subject_confidence', adjusted, threshold, True, 'validates subject confidence',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_subject_dependency_threshold', 27.0)
    return _result('check_subject_dependency', adjusted, threshold, True, 'validates subject dependency',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_subject_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'subject')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_subject_readiness_threshold', 29.333)
    return _result('check_subject_readiness', adjusted, threshold, False, 'validates subject readiness',
                   {'field': 'subject', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_learner_count_presence_threshold', 31.667)
    return _result('check_learner_count_presence', adjusted, threshold, True, 'validates learner_count presence',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_learner_count_range_threshold', 9.667)
    return _result('check_learner_count_range', adjusted, threshold, True, 'validates learner_count range',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_learner_count_stability_threshold', 12.0)
    return _result('check_learner_count_stability', adjusted, threshold, False, 'validates learner_count stability',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_learner_count_freshness_threshold', 14.333)
    return _result('check_learner_count_freshness', adjusted, threshold, True, 'validates learner_count freshness',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_learner_count_coverage_threshold', 16.667)
    return _result('check_learner_count_coverage', adjusted, threshold, True, 'validates learner_count coverage',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_learner_count_consistency_threshold', 19.0)
    return _result('check_learner_count_consistency', adjusted, threshold, False, 'validates learner_count consistency',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_learner_count_risk_threshold', 21.333)
    return _result('check_learner_count_risk', adjusted, threshold, True, 'validates learner_count risk',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_learner_count_confidence_threshold', 23.667)
    return _result('check_learner_count_confidence', adjusted, threshold, True, 'validates learner_count confidence',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_learner_count_dependency_threshold', 26.0)
    return _result('check_learner_count_dependency', adjusted, threshold, False, 'validates learner_count dependency',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_learner_count_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'learner_count')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_learner_count_readiness_threshold', 28.333)
    return _result('check_learner_count_readiness', adjusted, threshold, True, 'validates learner_count readiness',
                   {'field': 'learner_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_usage_minutes_presence_threshold', 30.667)
    return _result('check_usage_minutes_presence', adjusted, threshold, True, 'validates usage_minutes presence',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_usage_minutes_range_threshold', 8.667)
    return _result('check_usage_minutes_range', adjusted, threshold, False, 'validates usage_minutes range',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_usage_minutes_stability_threshold', 11.0)
    return _result('check_usage_minutes_stability', adjusted, threshold, True, 'validates usage_minutes stability',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_usage_minutes_freshness_threshold', 13.333)
    return _result('check_usage_minutes_freshness', adjusted, threshold, True, 'validates usage_minutes freshness',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_usage_minutes_coverage_threshold', 15.667)
    return _result('check_usage_minutes_coverage', adjusted, threshold, False, 'validates usage_minutes coverage',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_usage_minutes_consistency_threshold', 18.0)
    return _result('check_usage_minutes_consistency', adjusted, threshold, True, 'validates usage_minutes consistency',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_usage_minutes_risk_threshold', 20.333)
    return _result('check_usage_minutes_risk', adjusted, threshold, True, 'validates usage_minutes risk',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_usage_minutes_confidence_threshold', 22.667)
    return _result('check_usage_minutes_confidence', adjusted, threshold, False, 'validates usage_minutes confidence',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_usage_minutes_dependency_threshold', 25.0)
    return _result('check_usage_minutes_dependency', adjusted, threshold, True, 'validates usage_minutes dependency',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_usage_minutes_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'usage_minutes')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_usage_minutes_readiness_threshold', 27.333)
    return _result('check_usage_minutes_readiness', adjusted, threshold, True, 'validates usage_minutes readiness',
                   {'field': 'usage_minutes', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_baseline_score_presence_threshold', 29.667)
    return _result('check_baseline_score_presence', adjusted, threshold, False, 'validates baseline_score presence',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_baseline_score_range_threshold', 32.0)
    return _result('check_baseline_score_range', adjusted, threshold, True, 'validates baseline_score range',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_baseline_score_stability_threshold', 10.0)
    return _result('check_baseline_score_stability', adjusted, threshold, True, 'validates baseline_score stability',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_baseline_score_freshness_threshold', 12.333)
    return _result('check_baseline_score_freshness', adjusted, threshold, False, 'validates baseline_score freshness',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_baseline_score_coverage_threshold', 14.667)
    return _result('check_baseline_score_coverage', adjusted, threshold, True, 'validates baseline_score coverage',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_baseline_score_consistency_threshold', 17.0)
    return _result('check_baseline_score_consistency', adjusted, threshold, True, 'validates baseline_score consistency',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_baseline_score_risk_threshold', 19.333)
    return _result('check_baseline_score_risk', adjusted, threshold, False, 'validates baseline_score risk',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_baseline_score_confidence_threshold', 21.667)
    return _result('check_baseline_score_confidence', adjusted, threshold, True, 'validates baseline_score confidence',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_baseline_score_dependency_threshold', 24.0)
    return _result('check_baseline_score_dependency', adjusted, threshold, True, 'validates baseline_score dependency',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_score_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_score')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_baseline_score_readiness_threshold', 26.333)
    return _result('check_baseline_score_readiness', adjusted, threshold, False, 'validates baseline_score readiness',
                   {'field': 'baseline_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_outcome_score_presence_threshold', 28.667)
    return _result('check_outcome_score_presence', adjusted, threshold, True, 'validates outcome_score presence',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_outcome_score_range_threshold', 31.0)
    return _result('check_outcome_score_range', adjusted, threshold, True, 'validates outcome_score range',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_outcome_score_stability_threshold', 9.0)
    return _result('check_outcome_score_stability', adjusted, threshold, False, 'validates outcome_score stability',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_outcome_score_freshness_threshold', 11.333)
    return _result('check_outcome_score_freshness', adjusted, threshold, True, 'validates outcome_score freshness',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_outcome_score_coverage_threshold', 13.667)
    return _result('check_outcome_score_coverage', adjusted, threshold, True, 'validates outcome_score coverage',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_outcome_score_consistency_threshold', 16.0)
    return _result('check_outcome_score_consistency', adjusted, threshold, False, 'validates outcome_score consistency',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_outcome_score_risk_threshold', 18.333)
    return _result('check_outcome_score_risk', adjusted, threshold, True, 'validates outcome_score risk',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_outcome_score_confidence_threshold', 20.667)
    return _result('check_outcome_score_confidence', adjusted, threshold, True, 'validates outcome_score confidence',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_outcome_score_dependency_threshold', 23.0)
    return _result('check_outcome_score_dependency', adjusted, threshold, False, 'validates outcome_score dependency',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_outcome_score_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'outcome_score')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_outcome_score_readiness_threshold', 25.333)
    return _result('check_outcome_score_readiness', adjusted, threshold, True, 'validates outcome_score readiness',
                   {'field': 'outcome_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_missing_rate_presence_threshold', 27.667)
    return _result('check_missing_rate_presence', adjusted, threshold, True, 'validates missing_rate presence',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_missing_rate_range_threshold', 30.0)
    return _result('check_missing_rate_range', adjusted, threshold, False, 'validates missing_rate range',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_missing_rate_stability_threshold', 8.0)
    return _result('check_missing_rate_stability', adjusted, threshold, True, 'validates missing_rate stability',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_missing_rate_freshness_threshold', 10.333)
    return _result('check_missing_rate_freshness', adjusted, threshold, True, 'validates missing_rate freshness',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_missing_rate_coverage_threshold', 12.667)
    return _result('check_missing_rate_coverage', adjusted, threshold, False, 'validates missing_rate coverage',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_missing_rate_consistency_threshold', 15.0)
    return _result('check_missing_rate_consistency', adjusted, threshold, True, 'validates missing_rate consistency',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_missing_rate_risk_threshold', 17.333)
    return _result('check_missing_rate_risk', adjusted, threshold, True, 'validates missing_rate risk',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_missing_rate_confidence_threshold', 19.667)
    return _result('check_missing_rate_confidence', adjusted, threshold, False, 'validates missing_rate confidence',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_missing_rate_dependency_threshold', 22.0)
    return _result('check_missing_rate_dependency', adjusted, threshold, True, 'validates missing_rate dependency',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_missing_rate_readiness_threshold', 24.333)
    return _result('check_missing_rate_readiness', adjusted, threshold, True, 'validates missing_rate readiness',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_teacher_support_presence_threshold', 26.667)
    return _result('check_teacher_support_presence', adjusted, threshold, False, 'validates teacher_support presence',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_teacher_support_range_threshold', 29.0)
    return _result('check_teacher_support_range', adjusted, threshold, True, 'validates teacher_support range',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_teacher_support_stability_threshold', 31.333)
    return _result('check_teacher_support_stability', adjusted, threshold, True, 'validates teacher_support stability',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_teacher_support_freshness_threshold', 9.333)
    return _result('check_teacher_support_freshness', adjusted, threshold, False, 'validates teacher_support freshness',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_teacher_support_coverage_threshold', 11.667)
    return _result('check_teacher_support_coverage', adjusted, threshold, True, 'validates teacher_support coverage',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_teacher_support_consistency_threshold', 14.0)
    return _result('check_teacher_support_consistency', adjusted, threshold, True, 'validates teacher_support consistency',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_teacher_support_risk_threshold', 16.333)
    return _result('check_teacher_support_risk', adjusted, threshold, False, 'validates teacher_support risk',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_teacher_support_confidence_threshold', 18.667)
    return _result('check_teacher_support_confidence', adjusted, threshold, True, 'validates teacher_support confidence',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_teacher_support_dependency_threshold', 21.0)
    return _result('check_teacher_support_dependency', adjusted, threshold, True, 'validates teacher_support dependency',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_teacher_support_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'teacher_support')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_teacher_support_readiness_threshold', 23.333)
    return _result('check_teacher_support_readiness', adjusted, threshold, False, 'validates teacher_support readiness',
                   {'field': 'teacher_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_connectivity_presence_threshold', 25.667)
    return _result('check_connectivity_presence', adjusted, threshold, True, 'validates connectivity presence',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_connectivity_range_threshold', 28.0)
    return _result('check_connectivity_range', adjusted, threshold, True, 'validates connectivity range',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_connectivity_stability_threshold', 30.333)
    return _result('check_connectivity_stability', adjusted, threshold, False, 'validates connectivity stability',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_connectivity_freshness_threshold', 8.333)
    return _result('check_connectivity_freshness', adjusted, threshold, True, 'validates connectivity freshness',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_connectivity_coverage_threshold', 10.667)
    return _result('check_connectivity_coverage', adjusted, threshold, True, 'validates connectivity coverage',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_connectivity_consistency_threshold', 13.0)
    return _result('check_connectivity_consistency', adjusted, threshold, False, 'validates connectivity consistency',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_connectivity_risk_threshold', 15.333)
    return _result('check_connectivity_risk', adjusted, threshold, True, 'validates connectivity risk',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_connectivity_confidence_threshold', 17.667)
    return _result('check_connectivity_confidence', adjusted, threshold, True, 'validates connectivity confidence',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_connectivity_dependency_threshold', 20.0)
    return _result('check_connectivity_dependency', adjusted, threshold, False, 'validates connectivity dependency',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_connectivity_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'connectivity')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_connectivity_readiness_threshold', 22.333)
    return _result('check_connectivity_readiness', adjusted, threshold, True, 'validates connectivity readiness',
                   {'field': 'connectivity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_language_group_presence_threshold', 24.667)
    return _result('check_language_group_presence', adjusted, threshold, True, 'validates language_group presence',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_language_group_range_threshold', 27.0)
    return _result('check_language_group_range', adjusted, threshold, False, 'validates language_group range',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_language_group_stability_threshold', 29.333)
    return _result('check_language_group_stability', adjusted, threshold, True, 'validates language_group stability',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_language_group_freshness_threshold', 31.667)
    return _result('check_language_group_freshness', adjusted, threshold, True, 'validates language_group freshness',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_language_group_coverage_threshold', 9.667)
    return _result('check_language_group_coverage', adjusted, threshold, False, 'validates language_group coverage',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_language_group_consistency_threshold', 12.0)
    return _result('check_language_group_consistency', adjusted, threshold, True, 'validates language_group consistency',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_language_group_risk_threshold', 14.333)
    return _result('check_language_group_risk', adjusted, threshold, True, 'validates language_group risk',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_language_group_confidence_threshold', 16.667)
    return _result('check_language_group_confidence', adjusted, threshold, False, 'validates language_group confidence',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_language_group_dependency_threshold', 19.0)
    return _result('check_language_group_dependency', adjusted, threshold, True, 'validates language_group dependency',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_language_group_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'language_group')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_language_group_readiness_threshold', 21.333)
    return _result('check_language_group_readiness', adjusted, threshold, True, 'validates language_group readiness',
                   {'field': 'language_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_consent_rate_presence_threshold', 23.667)
    return _result('check_consent_rate_presence', adjusted, threshold, False, 'validates consent_rate presence',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_consent_rate_range_threshold', 26.0)
    return _result('check_consent_rate_range', adjusted, threshold, True, 'validates consent_rate range',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_consent_rate_stability_threshold', 28.333)
    return _result('check_consent_rate_stability', adjusted, threshold, True, 'validates consent_rate stability',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_consent_rate_freshness_threshold', 30.667)
    return _result('check_consent_rate_freshness', adjusted, threshold, False, 'validates consent_rate freshness',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_consent_rate_coverage_threshold', 8.667)
    return _result('check_consent_rate_coverage', adjusted, threshold, True, 'validates consent_rate coverage',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_consent_rate_consistency_threshold', 11.0)
    return _result('check_consent_rate_consistency', adjusted, threshold, True, 'validates consent_rate consistency',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_consent_rate_risk_threshold', 13.333)
    return _result('check_consent_rate_risk', adjusted, threshold, False, 'validates consent_rate risk',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_consent_rate_confidence_threshold', 15.667)
    return _result('check_consent_rate_confidence', adjusted, threshold, True, 'validates consent_rate confidence',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_consent_rate_dependency_threshold', 18.0)
    return _result('check_consent_rate_dependency', adjusted, threshold, True, 'validates consent_rate dependency',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_consent_rate_readiness_threshold', 20.333)
    return _result('check_consent_rate_readiness', adjusted, threshold, False, 'validates consent_rate readiness',
                   {'field': 'consent_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

RULES: tuple[RuleFunction, ...] = (
    check_school_code_presence,
    check_school_code_range,
    check_school_code_stability,
    check_school_code_freshness,
    check_school_code_coverage,
    check_school_code_consistency,
    check_school_code_risk,
    check_school_code_confidence,
    check_school_code_dependency,
    check_school_code_readiness,
    check_grade_band_presence,
    check_grade_band_range,
    check_grade_band_stability,
    check_grade_band_freshness,
    check_grade_band_coverage,
    check_grade_band_consistency,
    check_grade_band_risk,
    check_grade_band_confidence,
    check_grade_band_dependency,
    check_grade_band_readiness,
    check_subject_presence,
    check_subject_range,
    check_subject_stability,
    check_subject_freshness,
    check_subject_coverage,
    check_subject_consistency,
    check_subject_risk,
    check_subject_confidence,
    check_subject_dependency,
    check_subject_readiness,
    check_learner_count_presence,
    check_learner_count_range,
    check_learner_count_stability,
    check_learner_count_freshness,
    check_learner_count_coverage,
    check_learner_count_consistency,
    check_learner_count_risk,
    check_learner_count_confidence,
    check_learner_count_dependency,
    check_learner_count_readiness,
    check_usage_minutes_presence,
    check_usage_minutes_range,
    check_usage_minutes_stability,
    check_usage_minutes_freshness,
    check_usage_minutes_coverage,
    check_usage_minutes_consistency,
    check_usage_minutes_risk,
    check_usage_minutes_confidence,
    check_usage_minutes_dependency,
    check_usage_minutes_readiness,
    check_baseline_score_presence,
    check_baseline_score_range,
    check_baseline_score_stability,
    check_baseline_score_freshness,
    check_baseline_score_coverage,
    check_baseline_score_consistency,
    check_baseline_score_risk,
    check_baseline_score_confidence,
    check_baseline_score_dependency,
    check_baseline_score_readiness,
    check_outcome_score_presence,
    check_outcome_score_range,
    check_outcome_score_stability,
    check_outcome_score_freshness,
    check_outcome_score_coverage,
    check_outcome_score_consistency,
    check_outcome_score_risk,
    check_outcome_score_confidence,
    check_outcome_score_dependency,
    check_outcome_score_readiness,
    check_missing_rate_presence,
    check_missing_rate_range,
    check_missing_rate_stability,
    check_missing_rate_freshness,
    check_missing_rate_coverage,
    check_missing_rate_consistency,
    check_missing_rate_risk,
    check_missing_rate_confidence,
    check_missing_rate_dependency,
    check_missing_rate_readiness,
    check_teacher_support_presence,
    check_teacher_support_range,
    check_teacher_support_stability,
    check_teacher_support_freshness,
    check_teacher_support_coverage,
    check_teacher_support_consistency,
    check_teacher_support_risk,
    check_teacher_support_confidence,
    check_teacher_support_dependency,
    check_teacher_support_readiness,
    check_connectivity_presence,
    check_connectivity_range,
    check_connectivity_stability,
    check_connectivity_freshness,
    check_connectivity_coverage,
    check_connectivity_consistency,
    check_connectivity_risk,
    check_connectivity_confidence,
    check_connectivity_dependency,
    check_connectivity_readiness,
    check_language_group_presence,
    check_language_group_range,
    check_language_group_stability,
    check_language_group_freshness,
    check_language_group_coverage,
    check_language_group_consistency,
    check_language_group_risk,
    check_language_group_confidence,
    check_language_group_dependency,
    check_language_group_readiness,
    check_consent_rate_presence,
    check_consent_rate_range,
    check_consent_rate_stability,
    check_consent_rate_freshness,
    check_consent_rate_coverage,
    check_consent_rate_consistency,
    check_consent_rate_risk,
    check_consent_rate_confidence,
    check_consent_rate_dependency,
    check_consent_rate_readiness,
)

RULE_INDEX = {rule.__name__: rule for rule in RULES}

def evaluate(record: DomainRecord, context: Mapping[str, Any] | None = None) -> tuple[RuleResult, ...]:
    context = context or {}
    return tuple(rule(record, context) for rule in RULES)

def summarize(results: tuple[RuleResult, ...]) -> dict[str, Any]:
    if not results:
        return {'score': 0.0, 'passed': 0, 'failed': 0, 'critical': 0}
    return {'score': sum(item.score for item in results) / len(results),
            'passed': sum(item.passed for item in results),
            'failed': sum(not item.passed for item in results),
            'critical': sum(item.severity == 'critical' for item in results)}
