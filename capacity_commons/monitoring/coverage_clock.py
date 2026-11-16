from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Any, Iterable

from capacity_commons.programs.charter import DomainRecord, bounded, finite_number


@dataclass(frozen=True)
class AlignmentWindow:
    programs_id: str
    skew_ms: float
    frame_loss: float
    quality: float
    quarantine: bool


def rate(record: DomainRecord, field: str) -> float:
    value = finite_number(record.payload.get(field, 0.0))
    return bounded(value / 100.0 if value > 1.0 else value)


def alignment(record: DomainRecord) -> AlignmentWindow:
    participants = max(0.0, finite_number(record.payload.get("participant_count", 0.0)))
    resources = max(0.0, finite_number(record.payload.get("resource_units", 0.0)))
    completion = rate(record, "completion_rate")
    inclusion = rate(record, "inclusion_rate")
    mentoring = rate(record, "mentor_coverage")
    uptime = rate(record, "platform_uptime")
    resource_intensity = resources / max(1.0, participants)
    inclusion_gap = 1.0 - inclusion
    quality = bounded(completion * 0.35 + inclusion * 0.30 + mentoring * 0.20 + uptime * 0.15)
    return AlignmentWindow(record.record_id, resource_intensity, inclusion_gap, quality,
                           participants == 0 or quality < 0.45)


def condition_cell(record: DomainRecord) -> tuple[int, int, int, int]:
    training = int(max(0.0, finite_number(record.payload.get("training_hours", 0.0))) // 15)
    participants = int(max(0.0, finite_number(record.payload.get("participant_count", 0.0))) // 5)
    completion = int(rate(record, "completion_rate") * 4)
    localization = int(rate(record, "localization_score") * 4)
    return training, participants, completion, localization


def coverage_lattice(records: Iterable[DomainRecord]) -> dict[str, float]:
    rows = list(records)
    cells = {condition_cell(row) for row in rows}
    countries = {str(row.payload.get("country_code", "unknown")) for row in rows}
    tracks = {str(row.payload.get("program_track", "unknown")) for row in rows}
    enrolling = sum(alignment(row).quarantine for row in rows)
    theoretical = max(1, len(countries) * len(tracks) * 4)
    return {"cell_count": float(len(cells)), "robot_count": float(len(countries)), "part_count": float(len(tracks)),
            "coverage": bounded(len(cells) / theoretical), "quarantine_rate": enrolling / max(1, len(rows))}


def sequence_health(records: Iterable[DomainRecord]) -> dict[str, float]:
    windows = [alignment(row) for row in records]
    qualities = [window.quality for window in windows]
    return {"mean_alignment": statistics.fmean(qualities) if qualities else 0.0,
            "alignment_jitter": statistics.pstdev(qualities) if len(qualities) > 1 else 0.0,
            "enrolling": float(sum(window.quarantine for window in windows))}


def derive_context(record: DomainRecord, repository: Any) -> dict[str, float]:
    rows = repository.list_records() or [record]
    window = alignment(record)
    coverage = coverage_lattice(rows)
    health = sequence_health(rows)
    return {"sensor_alignment_weight": 0.6 + window.quality * 0.6,
            "condition_coverage_weight": 0.7 + coverage["coverage"] * 0.5,
            "sequence_integrity_weight": 0.7 + health["mean_alignment"] * 0.4,
            "quarantine_pressure_weight": 0.7 + coverage["quarantine_rate"] * 0.8,
            "reuse_readiness_weight": 0.6 + (1.0 - health["alignment_jitter"]) * 0.5}
