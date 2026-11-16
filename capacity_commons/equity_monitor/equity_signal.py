from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

@dataclass(frozen=True)
class DomainSignal:
    code: str
    score: float
    severity: str
    evidence: dict[str, Any]

def number(payload: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = float(payload.get(key, default))
    except (TypeError, ValueError):
        return default
    return default if value != value or value in (float('inf'), float('-inf')) else value

def ratio(payload: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = number(payload, key, default)
    if value > 1.0:
        value /= 100.0
    return max(0.0, min(1.0, value))

def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))

def equity_signal(payload: Mapping[str, Any]) -> DomainSignal:
    completion = ratio(payload, 'completion_rate')
    inclusion = ratio(payload, 'inclusion_rate')
    localization = ratio(payload, 'localization_score')
    mentors = ratio(payload, 'mentor_coverage')
    uptime = ratio(payload, 'platform_uptime')
    participants = max(1.0, number(payload, 'participant_count', 1.0))
    resources = max(0.0, number(payload, 'resource_units'))
    training = max(0.0, number(payload, 'training_hours'))
    reach = min(1.0, participants / 250.0)
    intensity = min(1.0, training / participants / 20.0)
    efficiency = 1.0 if resources == 0 else min(1.0, participants / resources / 8.0)
    floor = min(inclusion, localization, mentors)
    score = clamp(floor * 0.38 + completion * 0.2 + uptime * 0.12 + reach * 0.1 + intensity * 0.1 + efficiency * 0.1)
    severity = 'critical' if floor < 0.2 else 'warning' if floor < 0.5 or score < 0.55 else 'info'
    return DomainSignal('equity_signal', score, severity, {'equity_floor': floor, 'completion': completion, 'reach': reach, 'resource_efficiency': efficiency})

def peer_distribution(records: Iterable[Any], group_field: str = 'country_code') -> dict[str, Any]:
    groups = {}
    for record in records:
        payload = getattr(record, 'payload', record); key = str(payload.get(group_field, 'unknown'))
        groups.setdefault(key, []).append(equity_signal(payload).score)
    averages = {key: sum(values) / len(values) for key, values in groups.items()}
    gap = max(averages.values()) - min(averages.values()) if averages else 0.0
    return {'countries': averages, 'equity_gap': gap, 'count': sum(len(v) for v in groups.values())}

def augment_context(record: Any, repository: Any) -> dict[str, Any]:
    signal = equity_signal(record.payload); peers = peer_distribution(repository.list_records())
    return {'domain_signal': signal.score, 'domain_severity': signal.severity, 'equity_gap': peers['equity_gap'], 'peer_count': peers['count']}
