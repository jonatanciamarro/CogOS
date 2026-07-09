import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.social.communication import SocialCommunicationBus, CognitiveMessage
from runtime.social.trust_network import AgentTrustNetwork
from runtime.social.knowledge_transfer import KnowledgeTransfer
from runtime.social.conflict_protocol import ConflictProtocol
from runtime.agents.agent import CognitiveAgent

class TestSocialCognition(unittest.TestCase):
    """
    TestSocialCognition verifies CognitiveMessage bus routing, local trust adjustments,
    lineage checking, and persistent dispute protocols.
    """
    def test_message_bus_delivery(self):
        bus = SocialCommunicationBus()
        msg = CognitiveMessage("AgentA", "AgentB", "cse://concept/c1")
        bus.transmit(msg)

        fetched = bus.fetch_messages("AgentB")
        self.assertEqual(len(fetched), 1)
        self.assertEqual(fetched[0].claim, "cse://concept/c1")
        
        # Second fetch should clear inbox
        self.assertEqual(len(bus.fetch_messages("AgentB")), 0)

    def test_knowledge_ingestion_with_trust_scaling(self):
        trust_net = AgentTrustNetwork("owner")

        # Scenario 1: Default trust (0.5), empty lineage (multiplier 0.5)
        # Expected: confidence * trust * lineage_multiplier = 0.8 * 0.5 * 0.5 = 0.20
        msg_no_lineage = CognitiveMessage("sender", "owner", "cse://claim", confidence=0.8)
        belief_1 = KnowledgeTransfer.ingest_claim("sender", msg_no_lineage, trust_net)
        self.assertAlmostEqual(belief_1.confidence, 0.20)

        # Scenario 2: Updated high trust (0.8), populated lineage (multiplier 1.0)
        # Expected: 0.8 * 0.8 * 1.0 = 0.64
        trust_net.update_trust("sender", reward=True) # 0.5 -> 0.55
        trust_net.trust_ratings["sender"] = 0.80      # force 0.80 for exact testing
        msg_lineage = CognitiveMessage("sender", "owner", "cse://claim", confidence=0.8, lineage=["cse://ev_1"])
        belief_2 = KnowledgeTransfer.ingest_claim("sender", msg_lineage, trust_net)
        self.assertAlmostEqual(belief_2.confidence, 0.64)

    def test_disagreement_contradiction_edge(self):
        agent = CognitiveAgent("AgentB")
        edge = ConflictProtocol.register_disagreement(agent, "AgentA", "einstein", "newton")

        # Check returned Property Graph edge parameters
        self.assertEqual(edge["relation"], "CONTRADICTION")
        self.assertEqual(edge["source"], "einstein")
        self.assertEqual(edge["target"], "newton")

        # Confirm event log registration
        self.assertEqual(agent.event_log.ledger[-1].event_type, "PERSISTENT_DISAGREEMENT")

if __name__ == "__main__":
    unittest.main()
