from __future__ import annotations

import statistics
from typing import Any, Iterable, Mapping

from capacity_commons.programs.charter import ContractError, DomainRecord, bounded, finite_number, stable_hash

SCHEMA = "capacity-commons/stratified-analysis@1"
MISSING_LABEL = "(missing)"
DIMENSION_FIELDS = ("country_code", "program_track")
MEASURE_FIELDS = ("participant_count", "completion_rate", "resource_units", "training_hours")
DEFAULT_MIN_RECORDS = 2
DEFAULT_MAX_MISSING_RATE = 0.25


def is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def dimension_value(record: DomainRecord, field: str) -> str:
    value = record.payload.get(field)
    if is_missing(value):
        return MISSING_LABEL
    return str(value)


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return float(value)
    if is_missing(value):
        return None
    try:
        return max(0.0, finite_number(value))
    except ContractError:
        return None


def _measure_values(record: DomainRecord) -> dict[str, float | None]:
    return {field: _numeric(record.payload.get(field)) for field in MEASURE_FIELDS}


def _rate(number: float) -> float:
    return bounded(number / 100.0 if number > 1.0 else number)


def _thresholds(context: Mapping[str, Any] | None) -> dict[str, Any]:
    context = context or {}
    min_records = int(finite_number(context.get("strata_min_records", DEFAULT_MIN_RECORDS)))
    max_missing = bounded(finite_number(context.get("strata_max_missing_rate", DEFAULT_MAX_MISSING_RATE)))
    return {"min_records": max(1, min_records), "max_missing_rate": max_missing}


def _build_row(key: str, dimensions: Mapping[str, str], members: list[DomainRecord],
               revisions: Mapping[str, int], thresholds: Mapping[str, Any]) -> dict[str, Any]:
    members = sorted(members, key=lambda record: record.record_id)
    measure_rows = [(record, _measure_values(record)) for record in members]
    records = len(measure_rows)
    cells_expected = records * len(MEASURE_FIELDS)
    missing_cells = sum(1 for _, values in measure_rows for field in MEASURE_FIELDS if values[field] is None)
    missing_rate = missing_cells / cells_expected if cells_expected else 0.0

    def observed(field: str) -> list[float]:
        return [values[field] for _, values in measure_rows if values[field] is not None]

    participants = observed("participant_count")
    completions = observed("completion_rate")
    resources = observed("resource_units")
    training = observed("training_hours")
    participants_total = sum(participants)
    resources_total = sum(resources)
    issues: list[str] = []
    if records < thresholds["min_records"]:
        issues.append(f"records {records} below minimum {thresholds['min_records']}")
    if missing_rate > thresholds["max_missing_rate"]:
        issues.append(f"missing_rate {missing_rate:.6f} above maximum {thresholds['max_missing_rate']:.6f}")
    if not participants:
        issues.append("participant_count not reported")
    if not completions:
        issues.append("completion_rate not reported")
    return {
        "key": key,
        "dimensions": dict(dimensions),
        "records": records,
        "record_ids": [record.record_id for record, _ in measure_rows],
        "corrected_records": sum(1 for record, _ in measure_rows if revisions.get(record.record_id, 0) > 0),
        "payload_revisions": sum(int(revisions.get(record.record_id, 0)) for record, _ in measure_rows),
        "cells_expected": cells_expected,
        "missing_cells": missing_cells,
        "missing_rate": missing_rate,
        "participants_reported": len(participants),
        "participants_total": participants_total,
        "participants_mean": participants_total / len(participants) if participants else None,
        "completion_reported": len(completions),
        "completion_mean": statistics.fmean(_rate(value) for value in completions) if completions else None,
        "resources_reported": len(resources),
        "resources_total": resources_total,
        "resource_per_participant": resources_total / participants_total if participants_total > 0 else None,
        "training_reported": len(training),
        "training_hours_total": sum(training),
        "evidence": "insufficient" if issues else "sufficient",
        "evidence_issues": issues,
        "rank": None,
        "rank_note": "",
    }


def _rank_rows(rows: list[dict[str, Any]]) -> None:
    sufficient = [row for row in rows if row["evidence"] == "sufficient"]
    sufficient.sort(key=lambda row: (-row["completion_mean"], -row["participants_total"], row["key"]))
    for rank, row in enumerate(sufficient, start=1):
        row["rank"] = rank
        row["rank_note"] = "ranked among sufficient-evidence strata only"
    for row in rows:
        if row["rank"] is None:
            row["rank_note"] = "not ranked: insufficient evidence"
    rows.sort(key=lambda row: row["key"])


def _level(dimension: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "dimension": dimension,
        "row_count": len(rows),
        "sufficient": sum(1 for row in rows if row["evidence"] == "sufficient"),
        "insufficient": sum(1 for row in rows if row["evidence"] != "sufficient"),
        "rows": rows,
    }


def _group(records: list[DomainRecord], fields: tuple[str, ...]) -> dict[tuple[str, ...], list[DomainRecord]]:
    groups: dict[tuple[str, ...], list[DomainRecord]] = {}
    for record in records:
        key = tuple(dimension_value(record, field) for field in fields)
        groups.setdefault(key, []).append(record)
    return groups


def stratified_analysis(records: Iterable[DomainRecord], revisions: Mapping[str, int] | None = None,
                        context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    revisions = revisions or {}
    thresholds = _thresholds(context)
    ordered = sorted(records, key=lambda record: record.record_id)
    scope_records = [{
        "record_id": record.record_id,
        "country_code": dimension_value(record, "country_code"),
        "program_track": dimension_value(record, "program_track"),
        "payload_hash": stable_hash(record.payload),
        "payload_revisions": int(revisions.get(record.record_id, 0)),
    } for record in ordered]
    scope = {
        "record_count": len(scope_records),
        "records_with_corrections": sum(1 for item in scope_records if item["payload_revisions"] > 0),
        "payload_revisions_total": sum(item["payload_revisions"] for item in scope_records),
        "records_missing_country": sum(1 for item in scope_records if item["country_code"] == MISSING_LABEL),
        "records_missing_track": sum(1 for item in scope_records if item["program_track"] == MISSING_LABEL),
        "records": scope_records,
        "scope_hash": stable_hash(scope_records),
    }

    def build_rows(groups: Mapping[tuple[str, ...], list[DomainRecord]], names: tuple[str, ...]) -> list[dict[str, Any]]:
        rows = []
        for values, members in groups.items():
            dimensions = dict(zip(names, values))
            rows.append(_build_row("/".join(values), dimensions, members, revisions, thresholds))
        _rank_rows(rows)
        return rows

    overall_rows = []
    if ordered:
        overall_rows = [_build_row("all", {}, ordered, revisions, thresholds)]
        _rank_rows(overall_rows)
    levels = {
        "overall": _level("overall", overall_rows),
        "country": _level("country_code", build_rows(_group(ordered, ("country_code",)), ("country_code",))),
        "track": _level("program_track", build_rows(_group(ordered, ("program_track",)), ("program_track",))),
        "country_track": _level("country_code+program_track", build_rows(_group(ordered, DIMENSION_FIELDS), DIMENSION_FIELDS)),
    }
    analysis: dict[str, Any] = {
        "schema": SCHEMA,
        "thresholds": thresholds,
        "scope": scope,
        "levels": levels,
    }
    analysis["analysis_hash"] = stable_hash(analysis)
    return analysis


def stratum_index(analysis: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["key"]: row for row in analysis["levels"]["country_track"]["rows"]}


def stratum_context(record: DomainRecord, analysis: Mapping[str, Any]) -> dict[str, Any]:
    key = "/".join(dimension_value(record, field) for field in DIMENSION_FIELDS)
    row = stratum_index(analysis).get(key)
    context: dict[str, Any] = {
        "stratum_key": key,
        "stratum_scope": analysis["scope"]["scope_hash"],
        "stratum_analysis": analysis["analysis_hash"],
    }
    if row is None:
        context["stratum_evidence"] = "unobserved"
        context["stratum_records"] = 0.0
        context["stratum_missing_rate"] = 1.0
    else:
        context["stratum_evidence"] = row["evidence"]
        context["stratum_records"] = float(row["records"])
        context["stratum_missing_rate"] = row["missing_rate"]
    return context


def gate_outcome(outcome: str, stratum_evidence: str) -> str:
    if stratum_evidence in {"insufficient", "unobserved"} and outcome == "approve":
        return "review"
    return outcome
