from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from capacity_commons.programs.charter import DomainRecord, RuleResult, bounded, finite_number, normalized_text

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

def check_country_code_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_country_code_presence_threshold', 10.333)
    return _result('check_country_code_presence', adjusted, threshold, True, 'validates country_code presence',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_country_code_range_threshold', 12.667)
    return _result('check_country_code_range', adjusted, threshold, True, 'validates country_code range',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_country_code_stability_threshold', 15.0)
    return _result('check_country_code_stability', adjusted, threshold, False, 'validates country_code stability',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_country_code_freshness_threshold', 17.333)
    return _result('check_country_code_freshness', adjusted, threshold, True, 'validates country_code freshness',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_country_code_coverage_threshold', 19.667)
    return _result('check_country_code_coverage', adjusted, threshold, True, 'validates country_code coverage',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_country_code_consistency_threshold', 22.0)
    return _result('check_country_code_consistency', adjusted, threshold, False, 'validates country_code consistency',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_country_code_risk_threshold', 24.333)
    return _result('check_country_code_risk', adjusted, threshold, True, 'validates country_code risk',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_country_code_confidence_threshold', 26.667)
    return _result('check_country_code_confidence', adjusted, threshold, True, 'validates country_code confidence',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_country_code_dependency_threshold', 29.0)
    return _result('check_country_code_dependency', adjusted, threshold, False, 'validates country_code dependency',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_code_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country_code')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_country_code_readiness_threshold', 31.333)
    return _result('check_country_code_readiness', adjusted, threshold, True, 'validates country_code readiness',
                   {'field': 'country_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_program_track_presence_threshold', 9.333)
    return _result('check_program_track_presence', adjusted, threshold, True, 'validates program_track presence',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_program_track_range_threshold', 11.667)
    return _result('check_program_track_range', adjusted, threshold, False, 'validates program_track range',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_program_track_stability_threshold', 14.0)
    return _result('check_program_track_stability', adjusted, threshold, True, 'validates program_track stability',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_program_track_freshness_threshold', 16.333)
    return _result('check_program_track_freshness', adjusted, threshold, True, 'validates program_track freshness',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_program_track_coverage_threshold', 18.667)
    return _result('check_program_track_coverage', adjusted, threshold, False, 'validates program_track coverage',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_program_track_consistency_threshold', 21.0)
    return _result('check_program_track_consistency', adjusted, threshold, True, 'validates program_track consistency',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_program_track_risk_threshold', 23.333)
    return _result('check_program_track_risk', adjusted, threshold, True, 'validates program_track risk',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_program_track_confidence_threshold', 25.667)
    return _result('check_program_track_confidence', adjusted, threshold, False, 'validates program_track confidence',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_program_track_dependency_threshold', 28.0)
    return _result('check_program_track_dependency', adjusted, threshold, True, 'validates program_track dependency',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_program_track_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'program_track')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_program_track_readiness_threshold', 30.333)
    return _result('check_program_track_readiness', adjusted, threshold, True, 'validates program_track readiness',
                   {'field': 'program_track', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_training_hours_presence_threshold', 8.333)
    return _result('check_training_hours_presence', adjusted, threshold, False, 'validates training_hours presence',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_training_hours_range_threshold', 10.667)
    return _result('check_training_hours_range', adjusted, threshold, True, 'validates training_hours range',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_training_hours_stability_threshold', 13.0)
    return _result('check_training_hours_stability', adjusted, threshold, True, 'validates training_hours stability',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_training_hours_freshness_threshold', 15.333)
    return _result('check_training_hours_freshness', adjusted, threshold, False, 'validates training_hours freshness',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_training_hours_coverage_threshold', 17.667)
    return _result('check_training_hours_coverage', adjusted, threshold, True, 'validates training_hours coverage',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_training_hours_consistency_threshold', 20.0)
    return _result('check_training_hours_consistency', adjusted, threshold, True, 'validates training_hours consistency',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_training_hours_risk_threshold', 22.333)
    return _result('check_training_hours_risk', adjusted, threshold, False, 'validates training_hours risk',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_training_hours_confidence_threshold', 24.667)
    return _result('check_training_hours_confidence', adjusted, threshold, True, 'validates training_hours confidence',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_training_hours_dependency_threshold', 27.0)
    return _result('check_training_hours_dependency', adjusted, threshold, True, 'validates training_hours dependency',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_training_hours_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'training_hours')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_training_hours_readiness_threshold', 29.333)
    return _result('check_training_hours_readiness', adjusted, threshold, False, 'validates training_hours readiness',
                   {'field': 'training_hours', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_participant_count_presence_threshold', 31.667)
    return _result('check_participant_count_presence', adjusted, threshold, True, 'validates participant_count presence',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_participant_count_range_threshold', 9.667)
    return _result('check_participant_count_range', adjusted, threshold, True, 'validates participant_count range',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_participant_count_stability_threshold', 12.0)
    return _result('check_participant_count_stability', adjusted, threshold, False, 'validates participant_count stability',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_participant_count_freshness_threshold', 14.333)
    return _result('check_participant_count_freshness', adjusted, threshold, True, 'validates participant_count freshness',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_participant_count_coverage_threshold', 16.667)
    return _result('check_participant_count_coverage', adjusted, threshold, True, 'validates participant_count coverage',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_participant_count_consistency_threshold', 19.0)
    return _result('check_participant_count_consistency', adjusted, threshold, False, 'validates participant_count consistency',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_participant_count_risk_threshold', 21.333)
    return _result('check_participant_count_risk', adjusted, threshold, True, 'validates participant_count risk',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_participant_count_confidence_threshold', 23.667)
    return _result('check_participant_count_confidence', adjusted, threshold, True, 'validates participant_count confidence',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_participant_count_dependency_threshold', 26.0)
    return _result('check_participant_count_dependency', adjusted, threshold, False, 'validates participant_count dependency',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_participant_count_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'participant_count')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_participant_count_readiness_threshold', 28.333)
    return _result('check_participant_count_readiness', adjusted, threshold, True, 'validates participant_count readiness',
                   {'field': 'participant_count', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_completion_rate_presence_threshold', 30.667)
    return _result('check_completion_rate_presence', adjusted, threshold, True, 'validates completion_rate presence',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_completion_rate_range_threshold', 8.667)
    return _result('check_completion_rate_range', adjusted, threshold, False, 'validates completion_rate range',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_completion_rate_stability_threshold', 11.0)
    return _result('check_completion_rate_stability', adjusted, threshold, True, 'validates completion_rate stability',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_completion_rate_freshness_threshold', 13.333)
    return _result('check_completion_rate_freshness', adjusted, threshold, True, 'validates completion_rate freshness',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_completion_rate_coverage_threshold', 15.667)
    return _result('check_completion_rate_coverage', adjusted, threshold, False, 'validates completion_rate coverage',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_completion_rate_consistency_threshold', 18.0)
    return _result('check_completion_rate_consistency', adjusted, threshold, True, 'validates completion_rate consistency',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_completion_rate_risk_threshold', 20.333)
    return _result('check_completion_rate_risk', adjusted, threshold, True, 'validates completion_rate risk',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_completion_rate_confidence_threshold', 22.667)
    return _result('check_completion_rate_confidence', adjusted, threshold, False, 'validates completion_rate confidence',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_completion_rate_dependency_threshold', 25.0)
    return _result('check_completion_rate_dependency', adjusted, threshold, True, 'validates completion_rate dependency',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_completion_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'completion_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_completion_rate_readiness_threshold', 27.333)
    return _result('check_completion_rate_readiness', adjusted, threshold, True, 'validates completion_rate readiness',
                   {'field': 'completion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_localization_score_presence_threshold', 29.667)
    return _result('check_localization_score_presence', adjusted, threshold, False, 'validates localization_score presence',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_localization_score_range_threshold', 32.0)
    return _result('check_localization_score_range', adjusted, threshold, True, 'validates localization_score range',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_localization_score_stability_threshold', 10.0)
    return _result('check_localization_score_stability', adjusted, threshold, True, 'validates localization_score stability',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_localization_score_freshness_threshold', 12.333)
    return _result('check_localization_score_freshness', adjusted, threshold, False, 'validates localization_score freshness',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_localization_score_coverage_threshold', 14.667)
    return _result('check_localization_score_coverage', adjusted, threshold, True, 'validates localization_score coverage',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_localization_score_consistency_threshold', 17.0)
    return _result('check_localization_score_consistency', adjusted, threshold, True, 'validates localization_score consistency',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_localization_score_risk_threshold', 19.333)
    return _result('check_localization_score_risk', adjusted, threshold, False, 'validates localization_score risk',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_localization_score_confidence_threshold', 21.667)
    return _result('check_localization_score_confidence', adjusted, threshold, True, 'validates localization_score confidence',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_localization_score_dependency_threshold', 24.0)
    return _result('check_localization_score_dependency', adjusted, threshold, True, 'validates localization_score dependency',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_localization_score_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'localization_score')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_localization_score_readiness_threshold', 26.333)
    return _result('check_localization_score_readiness', adjusted, threshold, False, 'validates localization_score readiness',
                   {'field': 'localization_score', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_mentor_coverage_presence_threshold', 28.667)
    return _result('check_mentor_coverage_presence', adjusted, threshold, True, 'validates mentor_coverage presence',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_mentor_coverage_range_threshold', 31.0)
    return _result('check_mentor_coverage_range', adjusted, threshold, True, 'validates mentor_coverage range',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_mentor_coverage_stability_threshold', 9.0)
    return _result('check_mentor_coverage_stability', adjusted, threshold, False, 'validates mentor_coverage stability',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_mentor_coverage_freshness_threshold', 11.333)
    return _result('check_mentor_coverage_freshness', adjusted, threshold, True, 'validates mentor_coverage freshness',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_mentor_coverage_coverage_threshold', 13.667)
    return _result('check_mentor_coverage_coverage', adjusted, threshold, True, 'validates mentor_coverage coverage',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_mentor_coverage_consistency_threshold', 16.0)
    return _result('check_mentor_coverage_consistency', adjusted, threshold, False, 'validates mentor_coverage consistency',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_mentor_coverage_risk_threshold', 18.333)
    return _result('check_mentor_coverage_risk', adjusted, threshold, True, 'validates mentor_coverage risk',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_mentor_coverage_confidence_threshold', 20.667)
    return _result('check_mentor_coverage_confidence', adjusted, threshold, True, 'validates mentor_coverage confidence',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_mentor_coverage_dependency_threshold', 23.0)
    return _result('check_mentor_coverage_dependency', adjusted, threshold, False, 'validates mentor_coverage dependency',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_mentor_coverage_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'mentor_coverage')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_mentor_coverage_readiness_threshold', 25.333)
    return _result('check_mentor_coverage_readiness', adjusted, threshold, True, 'validates mentor_coverage readiness',
                   {'field': 'mentor_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_platform_uptime_presence_threshold', 27.667)
    return _result('check_platform_uptime_presence', adjusted, threshold, True, 'validates platform_uptime presence',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_platform_uptime_range_threshold', 30.0)
    return _result('check_platform_uptime_range', adjusted, threshold, False, 'validates platform_uptime range',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_platform_uptime_stability_threshold', 8.0)
    return _result('check_platform_uptime_stability', adjusted, threshold, True, 'validates platform_uptime stability',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_platform_uptime_freshness_threshold', 10.333)
    return _result('check_platform_uptime_freshness', adjusted, threshold, True, 'validates platform_uptime freshness',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_platform_uptime_coverage_threshold', 12.667)
    return _result('check_platform_uptime_coverage', adjusted, threshold, False, 'validates platform_uptime coverage',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_platform_uptime_consistency_threshold', 15.0)
    return _result('check_platform_uptime_consistency', adjusted, threshold, True, 'validates platform_uptime consistency',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_platform_uptime_risk_threshold', 17.333)
    return _result('check_platform_uptime_risk', adjusted, threshold, True, 'validates platform_uptime risk',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_platform_uptime_confidence_threshold', 19.667)
    return _result('check_platform_uptime_confidence', adjusted, threshold, False, 'validates platform_uptime confidence',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_platform_uptime_dependency_threshold', 22.0)
    return _result('check_platform_uptime_dependency', adjusted, threshold, True, 'validates platform_uptime dependency',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_platform_uptime_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'platform_uptime')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_platform_uptime_readiness_threshold', 24.333)
    return _result('check_platform_uptime_readiness', adjusted, threshold, True, 'validates platform_uptime readiness',
                   {'field': 'platform_uptime', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_resource_units_presence_threshold', 26.667)
    return _result('check_resource_units_presence', adjusted, threshold, False, 'validates resource_units presence',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_resource_units_range_threshold', 29.0)
    return _result('check_resource_units_range', adjusted, threshold, True, 'validates resource_units range',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_resource_units_stability_threshold', 31.333)
    return _result('check_resource_units_stability', adjusted, threshold, True, 'validates resource_units stability',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_resource_units_freshness_threshold', 9.333)
    return _result('check_resource_units_freshness', adjusted, threshold, False, 'validates resource_units freshness',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_resource_units_coverage_threshold', 11.667)
    return _result('check_resource_units_coverage', adjusted, threshold, True, 'validates resource_units coverage',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_resource_units_consistency_threshold', 14.0)
    return _result('check_resource_units_consistency', adjusted, threshold, True, 'validates resource_units consistency',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_resource_units_risk_threshold', 16.333)
    return _result('check_resource_units_risk', adjusted, threshold, False, 'validates resource_units risk',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_resource_units_confidence_threshold', 18.667)
    return _result('check_resource_units_confidence', adjusted, threshold, True, 'validates resource_units confidence',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_resource_units_dependency_threshold', 21.0)
    return _result('check_resource_units_dependency', adjusted, threshold, True, 'validates resource_units dependency',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_resource_units_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'resource_units')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_resource_units_readiness_threshold', 23.333)
    return _result('check_resource_units_readiness', adjusted, threshold, False, 'validates resource_units readiness',
                   {'field': 'resource_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_inclusion_rate_presence_threshold', 25.667)
    return _result('check_inclusion_rate_presence', adjusted, threshold, True, 'validates inclusion_rate presence',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_inclusion_rate_range_threshold', 28.0)
    return _result('check_inclusion_rate_range', adjusted, threshold, True, 'validates inclusion_rate range',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_inclusion_rate_stability_threshold', 30.333)
    return _result('check_inclusion_rate_stability', adjusted, threshold, False, 'validates inclusion_rate stability',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_inclusion_rate_freshness_threshold', 8.333)
    return _result('check_inclusion_rate_freshness', adjusted, threshold, True, 'validates inclusion_rate freshness',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_inclusion_rate_coverage_threshold', 10.667)
    return _result('check_inclusion_rate_coverage', adjusted, threshold, True, 'validates inclusion_rate coverage',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_inclusion_rate_consistency_threshold', 13.0)
    return _result('check_inclusion_rate_consistency', adjusted, threshold, False, 'validates inclusion_rate consistency',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_inclusion_rate_risk_threshold', 15.333)
    return _result('check_inclusion_rate_risk', adjusted, threshold, True, 'validates inclusion_rate risk',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_inclusion_rate_confidence_threshold', 17.667)
    return _result('check_inclusion_rate_confidence', adjusted, threshold, True, 'validates inclusion_rate confidence',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_inclusion_rate_dependency_threshold', 20.0)
    return _result('check_inclusion_rate_dependency', adjusted, threshold, False, 'validates inclusion_rate dependency',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_inclusion_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'inclusion_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_inclusion_rate_readiness_threshold', 22.333)
    return _result('check_inclusion_rate_readiness', adjusted, threshold, True, 'validates inclusion_rate readiness',
                   {'field': 'inclusion_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_partner_code_presence_threshold', 24.667)
    return _result('check_partner_code_presence', adjusted, threshold, True, 'validates partner_code presence',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_partner_code_range_threshold', 27.0)
    return _result('check_partner_code_range', adjusted, threshold, False, 'validates partner_code range',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_partner_code_stability_threshold', 29.333)
    return _result('check_partner_code_stability', adjusted, threshold, True, 'validates partner_code stability',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_partner_code_freshness_threshold', 31.667)
    return _result('check_partner_code_freshness', adjusted, threshold, True, 'validates partner_code freshness',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_partner_code_coverage_threshold', 9.667)
    return _result('check_partner_code_coverage', adjusted, threshold, False, 'validates partner_code coverage',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_partner_code_consistency_threshold', 12.0)
    return _result('check_partner_code_consistency', adjusted, threshold, True, 'validates partner_code consistency',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_partner_code_risk_threshold', 14.333)
    return _result('check_partner_code_risk', adjusted, threshold, True, 'validates partner_code risk',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_partner_code_confidence_threshold', 16.667)
    return _result('check_partner_code_confidence', adjusted, threshold, False, 'validates partner_code confidence',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_partner_code_dependency_threshold', 19.0)
    return _result('check_partner_code_dependency', adjusted, threshold, True, 'validates partner_code dependency',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_partner_code_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'partner_code')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_partner_code_readiness_threshold', 21.333)
    return _result('check_partner_code_readiness', adjusted, threshold, True, 'validates partner_code readiness',
                   {'field': 'partner_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_consent_scope_presence_threshold', 23.667)
    return _result('check_consent_scope_presence', adjusted, threshold, False, 'validates consent_scope presence',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_consent_scope_range_threshold', 26.0)
    return _result('check_consent_scope_range', adjusted, threshold, True, 'validates consent_scope range',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_consent_scope_stability_threshold', 28.333)
    return _result('check_consent_scope_stability', adjusted, threshold, True, 'validates consent_scope stability',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_consent_scope_freshness_threshold', 30.667)
    return _result('check_consent_scope_freshness', adjusted, threshold, False, 'validates consent_scope freshness',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_consent_scope_coverage_threshold', 8.667)
    return _result('check_consent_scope_coverage', adjusted, threshold, True, 'validates consent_scope coverage',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_consent_scope_consistency_threshold', 11.0)
    return _result('check_consent_scope_consistency', adjusted, threshold, True, 'validates consent_scope consistency',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_consent_scope_risk_threshold', 13.333)
    return _result('check_consent_scope_risk', adjusted, threshold, False, 'validates consent_scope risk',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_consent_scope_confidence_threshold', 15.667)
    return _result('check_consent_scope_confidence', adjusted, threshold, True, 'validates consent_scope confidence',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_consent_scope_dependency_threshold', 18.0)
    return _result('check_consent_scope_dependency', adjusted, threshold, True, 'validates consent_scope dependency',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_consent_scope_readiness_threshold', 20.333)
    return _result('check_consent_scope_readiness', adjusted, threshold, False, 'validates consent_scope readiness',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

RULES: tuple[RuleFunction, ...] = (
    check_country_code_presence,
    check_country_code_range,
    check_country_code_stability,
    check_country_code_freshness,
    check_country_code_coverage,
    check_country_code_consistency,
    check_country_code_risk,
    check_country_code_confidence,
    check_country_code_dependency,
    check_country_code_readiness,
    check_program_track_presence,
    check_program_track_range,
    check_program_track_stability,
    check_program_track_freshness,
    check_program_track_coverage,
    check_program_track_consistency,
    check_program_track_risk,
    check_program_track_confidence,
    check_program_track_dependency,
    check_program_track_readiness,
    check_training_hours_presence,
    check_training_hours_range,
    check_training_hours_stability,
    check_training_hours_freshness,
    check_training_hours_coverage,
    check_training_hours_consistency,
    check_training_hours_risk,
    check_training_hours_confidence,
    check_training_hours_dependency,
    check_training_hours_readiness,
    check_participant_count_presence,
    check_participant_count_range,
    check_participant_count_stability,
    check_participant_count_freshness,
    check_participant_count_coverage,
    check_participant_count_consistency,
    check_participant_count_risk,
    check_participant_count_confidence,
    check_participant_count_dependency,
    check_participant_count_readiness,
    check_completion_rate_presence,
    check_completion_rate_range,
    check_completion_rate_stability,
    check_completion_rate_freshness,
    check_completion_rate_coverage,
    check_completion_rate_consistency,
    check_completion_rate_risk,
    check_completion_rate_confidence,
    check_completion_rate_dependency,
    check_completion_rate_readiness,
    check_localization_score_presence,
    check_localization_score_range,
    check_localization_score_stability,
    check_localization_score_freshness,
    check_localization_score_coverage,
    check_localization_score_consistency,
    check_localization_score_risk,
    check_localization_score_confidence,
    check_localization_score_dependency,
    check_localization_score_readiness,
    check_mentor_coverage_presence,
    check_mentor_coverage_range,
    check_mentor_coverage_stability,
    check_mentor_coverage_freshness,
    check_mentor_coverage_coverage,
    check_mentor_coverage_consistency,
    check_mentor_coverage_risk,
    check_mentor_coverage_confidence,
    check_mentor_coverage_dependency,
    check_mentor_coverage_readiness,
    check_platform_uptime_presence,
    check_platform_uptime_range,
    check_platform_uptime_stability,
    check_platform_uptime_freshness,
    check_platform_uptime_coverage,
    check_platform_uptime_consistency,
    check_platform_uptime_risk,
    check_platform_uptime_confidence,
    check_platform_uptime_dependency,
    check_platform_uptime_readiness,
    check_resource_units_presence,
    check_resource_units_range,
    check_resource_units_stability,
    check_resource_units_freshness,
    check_resource_units_coverage,
    check_resource_units_consistency,
    check_resource_units_risk,
    check_resource_units_confidence,
    check_resource_units_dependency,
    check_resource_units_readiness,
    check_inclusion_rate_presence,
    check_inclusion_rate_range,
    check_inclusion_rate_stability,
    check_inclusion_rate_freshness,
    check_inclusion_rate_coverage,
    check_inclusion_rate_consistency,
    check_inclusion_rate_risk,
    check_inclusion_rate_confidence,
    check_inclusion_rate_dependency,
    check_inclusion_rate_readiness,
    check_partner_code_presence,
    check_partner_code_range,
    check_partner_code_stability,
    check_partner_code_freshness,
    check_partner_code_coverage,
    check_partner_code_consistency,
    check_partner_code_risk,
    check_partner_code_confidence,
    check_partner_code_dependency,
    check_partner_code_readiness,
    check_consent_scope_presence,
    check_consent_scope_range,
    check_consent_scope_stability,
    check_consent_scope_freshness,
    check_consent_scope_coverage,
    check_consent_scope_consistency,
    check_consent_scope_risk,
    check_consent_scope_confidence,
    check_consent_scope_dependency,
    check_consent_scope_readiness,
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
