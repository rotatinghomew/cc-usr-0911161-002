from __future__ import annotations

import unittest
from capacity_commons.programs.charter import DomainRecord
from capacity_commons.monitoring.coverage_clock import alignment, condition_cell, coverage_lattice, sequence_health


class TimelineTests(unittest.TestCase):
    def record(self, key, completion=85, inclusion=80):
        return DomainRecord(key, {"country_code": "r1", "program_track": "mentoring", "training_hours": 32, "participant_count": 40,
            "completion_rate": completion, "localization_score": 80, "mentor_coverage": 75, "platform_uptime": 95,
            "resource_units": 5, "inclusion_rate": inclusion, "partner_code": "op", "consent_scope": "training"})

    def test_insufficient_participation_evidence_is_flagged(self):
        self.assertFalse(alignment(self.record("a")).quarantine)
        self.assertTrue(alignment(self.record("b", completion=20, inclusion=10)).quarantine)

    def test_lattice_and_sequence_health(self):
        rows = [self.record("a"), self.record("b", completion=20, inclusion=0)]
        self.assertEqual(len(condition_cell(rows[0])), 4)
        self.assertGreater(coverage_lattice(rows)["cell_count"], 0)
        self.assertEqual(sequence_health(rows)["enrolling"], 1.0)
