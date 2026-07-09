import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.culture.memes import CognitiveMeme
from runtime.culture.tradition import CultureTradition
from runtime.culture.reputation import HistoricalReputation
from runtime.culture.protocol import EmergentProtocol
from runtime.agents.agent import CognitiveAgent

class TestCognitiveCulture(unittest.TestCase):
    """
    TestCognitiveCulture verifies CognitiveMeme adoption increments, tradition copying paths,
    reputation calculations, and EmergentProtocol symbol translation dictionaries.
    """
    def test_meme_replication(self):
        meme = CognitiveMeme("meme_1", "CsaMethod", "agent_A")
        self.assertEqual(meme.adoption_count, 1)

        meme.increment_adoption()
        self.assertEqual(meme.adoption_count, 2)

    def test_cultural_tradition_inheritance(self):
        parent = CognitiveAgent("ParentTeacher")
        child = CognitiveAgent("ChildApprentice")

        parent.strategy_memory.add_strategy("tradition_use_csa_verification")
        parent.strategy_memory.add_strategy("ad_hoc_plan_x")

        # Inherit parent traditions
        inherited_count = CultureTradition.inherit_traditions(parent, child)
        
        self.assertEqual(inherited_count, 1)
        self.assertEqual(len(child.strategy_memory.logs), 1)
        self.assertEqual(child.strategy_memory.logs[0], "tradition_use_csa_verification")

    def test_historical_reputation_audit(self):
        reputation = HistoricalReputation()
        agent_id = "agent_X"

        # Default trust evaluation
        self.assertEqual(reputation.get_reputation(agent_id), 0.50)

        # Log proposals and commits
        reputation.record_proposal(agent_id)
        reputation.record_proposal(agent_id)
        reputation.record_commit(agent_id)

        # 1 commit out of 2 proposals = 0.50 reputation
        self.assertEqual(reputation.get_reputation(agent_id), 0.50)

        reputation.record_commit(agent_id)
        # 2 commits out of 2 proposals = 1.00 reputation
        self.assertEqual(reputation.get_reputation(agent_id), 1.00)

    def test_protocol_symbol_translations(self):
        protocol = EmergentProtocol()

        # Map concept URI
        symbol1 = protocol.translate_to_symbol("cse://concept/complex_thermodynamics")
        symbol2 = protocol.translate_to_symbol("cse://concept/complex_thermodynamics")

        # Same symbol returned for matching URI
        self.assertEqual(symbol1, symbol2)
        self.assertEqual(symbol1, "SYM_001")

        # Reverse resolution
        resolved = protocol.translate_to_uri("SYM_001")
        self.assertEqual(resolved, "cse://concept/complex_thermodynamics")

if __name__ == "__main__":
    unittest.main()
