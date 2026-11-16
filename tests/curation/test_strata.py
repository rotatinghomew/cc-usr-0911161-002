from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from capacity_commons.programs.charter import DomainRecord, records_from_fixture, stable_hash
from capacity_commons.curation.strata import (MISSING_LABEL, dimension_value, gate_outcome,
                                              stratified_analysis, stratum_context)
from capacity_commons.outcomes.program_cycle import decide
from capacity_commons.grants.allocation_ledger import Repository
from capacity_commons.program_office import Application, run, verify
from capacity_commons.outcomes.impact_manifest import verify_bundle

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "acceptance.json"


def make_record(record_id: str, country: str = "country-a", track: str = "track-a",
                participants=100.0, completion=80.0, resources=20.0, training=40.0,
                extra: dict | None = None) -> DomainRecord:
    payload = {
        "country_code": country, "program_track": track,
        "training_hours": training, "participant_count": participants,
        "completion_rate": completion, "localization_score": 70.0,
        "mentor_coverage": 60.0, "platform_uptime": 90.0,
        "resource_units": resources, "inclusion_rate": 75.0,
        "partner_code": "partner-a", "consent_scope": "aggregate",
    }
    if extra:
        payload.update(extra)
    return DomainRecord(record_id, payload, "proposed")


def cell_row(analysis: dict, country: str, track: str) -> dict:
    key = f"{country}/{track}"
    for row in analysis["levels"]["country_track"]["rows"]:
        if row["key"] == key:
            return row
    raise AssertionError(f"missing stratum {key}")


class ScopeTests(unittest.TestCase):
    def test_scope_counts_unique_records_not_corrections(self):
        records = [make_record("r1"), make_record("r2")]
        analysis = stratified_analysis(records, {"r1": 2})
        scope = analysis["scope"]
        self.assertEqual(scope["record_count"], 2)
        self.assertEqual(scope["records_with_corrections"], 1)
        self.assertEqual(scope["payload_revisions_total"], 2)
        row = cell_row(analysis, "country-a", "track-a")
        self.assertEqual(row["records"], 2)
        self.assertEqual(row["corrected_records"], 1)

    def test_scope_hash_tracks_payloads_not_workflow_versions(self):
        record = make_record("r1")
        advanced = record.with_state("funded")
        self.assertNotEqual(record.version, advanced.version)
        first = stratified_analysis([record], {"r1": 0})
        second = stratified_analysis([advanced], {"r1": 0})
        self.assertEqual(first["scope"]["scope_hash"], second["scope"]["scope_hash"])
        self.assertEqual(first["analysis_hash"], second["analysis_hash"])
        corrected = stratified_analysis([record.with_payload({"participant_count": 150.0})], {"r1": 1})
        self.assertNotEqual(first["scope"]["scope_hash"], corrected["scope"]["scope_hash"])
        self.assertNotEqual(first["analysis_hash"], corrected["analysis_hash"])

    def test_missing_dimensions_are_labelled(self):
        record = make_record("r1", extra={"country_code": None})
        analysis = stratified_analysis([record])
        self.assertEqual(analysis["scope"]["records_missing_country"], 1)
        self.assertEqual(dimension_value(record, "country_code"), MISSING_LABEL)
        keys = {row["key"] for row in analysis["levels"]["country"]["rows"]}
        self.assertIn(MISSING_LABEL, keys)


class StratumStatsTests(unittest.TestCase):
    def test_denominators_and_missingness_are_explicit(self):
        records = [
            make_record("r1", completion=80.0),
            make_record("r2", extra={"completion_rate": None}),
        ]
        row = cell_row(stratified_analysis(records), "country-a", "track-a")
        self.assertEqual(row["records"], 2)
        self.assertEqual(row["completion_reported"], 1)
        self.assertEqual(row["completion_mean"], 0.8)
        self.assertEqual(row["participants_reported"], 2)
        self.assertEqual(row["missing_cells"], 1)
        self.assertEqual(row["cells_expected"], 8)
        self.assertAlmostEqual(row["missing_rate"], 1 / 8)

    def test_completion_and_resources_compared_on_same_scope(self):
        records = [
            make_record("r1", participants=100.0, completion=80.0, resources=20.0),
            make_record("r2", participants=300.0, completion=40.0, resources=60.0),
        ]
        row = cell_row(stratified_analysis(records), "country-a", "track-a")
        self.assertEqual(row["participants_total"], 400.0)
        self.assertAlmostEqual(row["completion_mean"], 0.6)
        self.assertEqual(row["resources_total"], 80.0)
        self.assertAlmostEqual(row["resource_per_participant"], 0.2)
        overall = stratified_analysis(records)["levels"]["overall"]["rows"][0]
        self.assertEqual(overall["participants_total"], row["participants_total"])
        self.assertEqual(overall["resources_total"], row["resources_total"])


class EvidenceGatingTests(unittest.TestCase):
    def test_small_stratum_is_not_ranked(self):
        records = [
            make_record("r1", country="country-a", track="track-a"),
            make_record("r2", country="country-a", track="track-a"),
            make_record("r3", country="country-b", track="track-b"),
        ]
        analysis = stratified_analysis(records)
        sufficient = cell_row(analysis, "country-a", "track-a")
        insufficient = cell_row(analysis, "country-b", "track-b")
        self.assertEqual(sufficient["evidence"], "sufficient")
        self.assertEqual(sufficient["rank"], 1)
        self.assertEqual(insufficient["evidence"], "insufficient")
        self.assertIsNone(insufficient["rank"])
        self.assertIn("not ranked", insufficient["rank_note"])
        self.assertTrue(any("below minimum" in issue for issue in insufficient["evidence_issues"]))

    def test_missing_heavy_stratum_is_not_ranked(self):
        empty = {"participant_count": None, "completion_rate": None,
                 "resource_units": None, "training_hours": None}
        records = [make_record("r1", extra=empty), make_record("r2", extra=empty)]
        row = cell_row(stratified_analysis(records), "country-a", "track-a")
        self.assertEqual(row["missing_rate"], 1.0)
        self.assertEqual(row["evidence"], "insufficient")
        self.assertIsNone(row["rank"])
        self.assertTrue(any("missing_rate" in issue for issue in row["evidence_issues"]))
        self.assertTrue(any("participant_count not reported" in issue for issue in row["evidence_issues"]))

    def test_ranking_only_among_sufficient_strata(self):
        records = [
            make_record("r1", country="country-a", track="track-a", completion=90.0),
            make_record("r2", country="country-a", track="track-a", completion=90.0),
            make_record("r3", country="country-b", track="track-b", completion=50.0),
            make_record("r4", country="country-b", track="track-b", completion=50.0),
            make_record("r5", country="country-c", track="track-c", completion=99.0),
        ]
        analysis = stratified_analysis(records)
        self.assertEqual(cell_row(analysis, "country-a", "track-a")["rank"], 1)
        self.assertEqual(cell_row(analysis, "country-b", "track-b")["rank"], 2)
        self.assertIsNone(cell_row(analysis, "country-c", "track-c")["rank"])
        level = analysis["levels"]["country_track"]
        self.assertEqual(level["sufficient"], 2)
        self.assertEqual(level["insufficient"], 1)

    def test_gate_outcome_caps_approve(self):
        self.assertEqual(gate_outcome("approve", "insufficient"), "review")
        self.assertEqual(gate_outcome("approve", "unobserved"), "review")
        self.assertEqual(gate_outcome("approve", "sufficient"), "approve")
        self.assertEqual(gate_outcome("approve", ""), "approve")
        self.assertEqual(gate_outcome("reject", "insufficient"), "reject")

    def test_decide_consumes_stratum_evidence(self):
        fields = ["country_code", "program_track", "training_hours", "participant_count",
                  "completion_rate", "localization_score", "mentor_coverage", "platform_uptime",
                  "resource_units", "inclusion_rate", "partner_code", "consent_scope"]
        values = [13.79, 11.98, 9.84, 10.62, 9.99, 12.33, 9.94, 15.1, 9.16, 17.15, 9.72, 9.12]
        record = DomainRecord("capacity_program-900", dict(zip(fields, values)), "proposed")
        baseline = decide(record, {"approve_threshold": 0.0})
        self.assertEqual(baseline.outcome, "approve")
        gated = decide(record, {"approve_threshold": 0.0, "stratum_key": "country-a/track-a",
                                "stratum_evidence": "insufficient", "stratum_scope": "ab" * 32})
        self.assertEqual(gated.outcome, "review")
        self.assertIn("stratum_evidence=insufficient", gated.reasons)
        self.assertEqual(set(gated.metrics), set(baseline.metrics))

    def test_decide_without_stratum_context_keeps_baseline_reasons(self):
        record = make_record("r1")
        decision = decide(record)
        self.assertEqual(len(decision.reasons), 3)
        self.assertFalse(any("stratum" in reason for reason in decision.reasons))


class RepositoryRevisionTests(unittest.TestCase):
    def test_payload_revisions_distinguish_corrections_from_state_advances(self):
        with tempfile.TemporaryDirectory() as temp:
            repository = Repository(Path(temp) / "state.sqlite3")
            record = make_record("r1")
            repository.save_record(record)
            self.assertEqual(repository.payload_revisions(), {})
            corrected = record.with_payload({"participant_count": 150.0})
            repository.save_record(corrected, expected_version=1)
            self.assertEqual(repository.payload_revisions(), {"r1": 1})
            advanced = corrected.with_state("funded")
            repository.save_record(advanced, expected_version=2)
            self.assertEqual(repository.payload_revisions(), {"r1": 1})


class EndToEndTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.database = self.root / "run.sqlite3"
        self.output = self.root / "output"

    def load_analysis(self) -> dict:
        return json.loads((self.output / "analysis.json").read_text(encoding="utf-8"))

    def test_run_exports_analysis_and_verifies(self):
        result = run(FIXTURE, self.database, self.output)
        analysis = self.load_analysis()
        self.assertEqual(result["analysis_hash"], analysis["analysis_hash"])
        self.assertEqual(result["scope_hash"], analysis["scope"]["scope_hash"])
        self.assertEqual(analysis["scope"]["record_count"], 8)
        self.assertEqual(analysis["scope"]["payload_revisions_total"], 0)
        self.assertEqual(set(analysis["levels"]), {"overall", "country", "track", "country_track"})
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("analysis.json", manifest["files"])
        self.assertEqual(verify_bundle(self.output), [])
        self.assertTrue(verify(self.database, self.output)["ok"])

    def test_repeated_run_keeps_same_analysis(self):
        first = run(FIXTURE, self.database, self.output)
        second = run(FIXTURE, self.database, self.output)
        self.assertEqual(first["run_id"], second["run_id"])
        self.assertEqual(first["analysis_hash"], second["analysis_hash"])
        self.assertEqual(first["scope_hash"], second["scope_hash"])

    def test_analyze_reproduces_bundle_analysis_after_run(self):
        run(FIXTURE, self.database, self.output)
        exported = self.load_analysis()
        recomputed = Application(self.database).analyze()
        self.assertEqual(recomputed["analysis_hash"], exported["analysis_hash"])
        self.assertEqual(recomputed["scope"]["scope_hash"], exported["scope"]["scope_hash"])

    def test_decisions_share_one_observation_scope(self):
        result = run(FIXTURE, self.database, self.output)
        decisions = json.loads((self.output / "decisions.json").read_text(encoding="utf-8"))
        expected = f"stratum_scope={result['scope_hash'][:12]}"
        self.assertTrue(decisions)
        for row in decisions:
            self.assertEqual(len(row["reasons"]), 6)
            self.assertEqual(row["reasons"][-1], expected)
            self.assertTrue(row["reasons"][-2].startswith("stratum_evidence="))

    def test_correction_produces_new_analysis_and_history_is_kept(self):
        first = run(FIXTURE, self.database, self.output)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["records"][0]["payload"]["participant_count"] = 18.7
        corrected_path = self.root / "corrected.json"
        corrected_path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        second = run(corrected_path, self.database, self.output)
        self.assertNotEqual(first["run_id"], second["run_id"])
        self.assertNotEqual(first["analysis_hash"], second["analysis_hash"])
        corrected = self.load_analysis()
        self.assertEqual(corrected["scope"]["record_count"], 8)
        self.assertEqual(corrected["scope"]["payload_revisions_total"], 1)
        self.assertEqual(corrected["scope"]["records_with_corrections"], 1)
        repository = Repository(self.database)
        self.assertEqual(repository.payload_revisions().get("capacity_program-001"), 1)
        stored = repository.completed_run(first["run_id"])
        self.assertIsNotNone(stored)
        self.assertEqual(stored["analysis_hash"], first["analysis_hash"])
        self.assertEqual(stored["analysis"]["analysis_hash"], first["analysis_hash"])
        self.assertTrue(verify(self.database, self.output)["ok"])


if __name__ == "__main__":
    unittest.main()
