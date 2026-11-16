from __future__ import annotations
import unittest
from capacity_commons.equity_monitor.equity_signal import equity_signal, peer_distribution
class Record:
    def __init__(self, payload): self.payload = payload
class SignalTests(unittest.TestCase):
    def setUp(self): self.payload = {'country_code': 'country-a', 'program_track': 'governance', 'training_hours': 800, 'participant_count': 120, 'completion_rate': 0.82, 'localization_score': 0.76, 'mentor_coverage': 0.7, 'platform_uptime': 0.96, 'resource_units': 18, 'inclusion_rate': 0.74, 'partner_code': 'partner-a', 'consent_scope': 'aggregate'}
    def test_signal_is_bounded_and_explainable(self):
        signal = equity_signal(self.payload)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)
        self.assertIn(signal.severity, {'info', 'warning', 'critical'})
        self.assertTrue({'completion', 'resource_efficiency', 'equity_floor'}.issubset(signal.evidence))
    def test_peer_distribution_uses_business_group(self):
        other = dict(self.payload); other['country_code'] = 'group-b'
        result = peer_distribution([Record(self.payload), Record(other)])
        self.assertEqual(result['count'], 2)
        self.assertIn('countries', result)
    def test_material_business_change_is_observable(self):
        changed = dict(self.payload); changed['inclusion_rate'] = 0.1
        self.assertNotEqual(equity_signal(changed).score, equity_signal(self.payload).score)
    def test_business_variant_1(self):
        changed = dict(self.payload)
        changed['training_hours'] = self.payload['training_hours']
        signal = equity_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_2(self):
        changed = dict(self.payload)
        changed['participant_count'] = self.payload['participant_count']
        signal = equity_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_3(self):
        changed = dict(self.payload)
        changed['completion_rate'] = self.payload['completion_rate']
        signal = equity_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_4(self):
        changed = dict(self.payload)
        changed['localization_score'] = self.payload['localization_score']
        signal = equity_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

if __name__ == '__main__': unittest.main()
