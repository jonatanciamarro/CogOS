import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.self_model.self_assessment import SelfAssessment
from runtime.self_model.metacognition import MetaCognitionEngine
from runtime.self_model.attention_economy import AttentionManager
from runtime.self_model.value_system import ValueSystem
from runtime.self_model.development import DevelopmentEngine
from runtime.intelligence.state_model import InternalBelief

class TestSelfModelSubstrate(unittest.TestCase):
    """
    TestSelfModelSubstrate verifies metacognitive belief audits, utility-based values arbitration,
    and capability self-assessment scaling.
    """
    def test_metacognitive_audit(self):
        metacog = MetaCognitionEngine()

        # Scenario 1: Inflated belief (high confidence, zero evidence)
        belief_inflated = InternalBelief("cse://concept/rule_x", confidence=0.8)
        corrected = metacog.audit_belief(belief_inflated)
        self.assertTrue(corrected)
        self.assertEqual(belief_inflated.confidence, 0.4)

        # Scenario 2: Supported belief (high confidence, sufficient evidence)
        belief_supported = InternalBelief("cse://concept/rule_y", confidence=0.8)
        belief_supported.evidence = ["obs_1", "obs_2", "obs_3"]
        corrected2 = metacog.audit_belief(belief_supported)
        self.assertFalse(corrected2)
        self.assertEqual(belief_supported.confidence, 0.8)

    def test_value_arbitration(self):
        values = ValueSystem(exploration_weight=0.8, preservation_weight=0.2)
        choices = [
            {"name": "goal_explore", "exploration_utility": 0.9, "preservation_utility": 0.1},
            {"name": "goal_preserve", "exploration_utility": 0.2, "preservation_utility": 0.9}
        ]
        winner = values.arbitrate(choices)
        self.assertEqual(winner["name"], "goal_explore")

    def test_self_assessment_decay(self):
        assessment = SelfAssessment()

        # Trial fails -> trust should drop from 0.5 to 0.3
        trust_after_fail = assessment.record_trial("instrument_read", success=False)
        self.assertAlmostEqual(trust_after_fail, 0.3)

        # Trial succeeds -> trust should recover from 0.3 to 0.4
        trust_after_success = assessment.record_trial("instrument_read", success=True)
        self.assertAlmostEqual(trust_after_success, 0.4)

if __name__ == "__main__":
    unittest.main()
