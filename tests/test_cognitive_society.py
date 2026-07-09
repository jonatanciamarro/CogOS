import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.cogos.boot import CogOSBootloader
from runtime.society.society import SocietyManager
from runtime.society.coalition import CoalitionEngine
from runtime.society.consensus import ConsensusEngine
from runtime.society.governance import Governance
from runtime.society.collective_memory import CollectiveMemory
from runtime.society.evolution import EvolutionEngine
from runtime.agents.lifecycle import AgentLifecycleManager
from runtime.agents.capability import Capability

class TestCognitiveSociety(unittest.TestCase):
    """
    TestCognitiveSociety validates dynamic coalition formation, reputation-evidence consensus metrics,
    governance compliance checks, and metric-based evolutionary spawning.
    """
    def test_coalition_formation(self):
        engine = CoalitionEngine()
        coalition = engine.form_coalition("TestCoal", "solve_math", ["agent_1", "agent_2"])
        self.assertEqual(len(coalition.members), 2)
        self.assertIn("agent_1", coalition.members)

    def test_weighted_consensus_scoring(self):
        # Voter 1: High trust (0.9), valid lineage (bonus) -> Agrees
        # Voter 2: Low trust (0.4), empty lineage -> Disagrees
        votes = [
            {"agent_id": "a1", "agree": True, "confidence": 0.80, "lineage_size": 2},
            {"agent_id": "a2", "agree": False, "confidence": 0.30, "lineage_size": 0}
        ]
        reputations = {"a1": 0.90, "a2": 0.40}
        
        score = ConsensusEngine.evaluate_proposal(votes, reputations)
        # a1 weight = 0.8 * 0.9 * 1.2 = 0.864
        # a2 weight = 0.3 * 0.4 * 1.0 = 0.12
        # Score = 0.864 / (0.864 + 0.12) = 0.878
        self.assertAlmostEqual(score, 0.864 / (0.864 + 0.12))
        self.assertGreater(score, 0.70)

    def test_governance_safety_audit(self):
        # Valid proposal passes
        self.assertTrue(Governance.audit_consensus_node("cse://concept/theory_x"))
        # Invalid proposal triggers bypass safety token -> Rejected
        self.assertFalse(Governance.audit_consensus_node("cse://concept/bypass_safety_invariants"))

    def test_evolutionary_uncertainty_trigger(self):
        kernel = CogOSBootloader.boot()
        lifecycle_manager = AgentLifecycleManager(kernel)
        evolution = EvolutionEngine(lifecycle_manager)

        parent = lifecycle_manager.spawn_agent("Parent")
        parent.add_capability(Capability("spawner", "E-EVOLVE"))

        # Global uncertainty is high (0.85) -> Spawns specialized agent
        child = evolution.check_evolution_trigger(system_uncertainty=0.85, parent_agent=parent)
        self.assertIsNotNone(child)
        self.assertEqual(child.identity.parent_id, parent.identity.agent_id)

if __name__ == "__main__":
    unittest.main()
