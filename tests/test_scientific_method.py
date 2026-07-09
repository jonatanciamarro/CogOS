import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.interfaces import ScienceProvider, HistoryProvider, CultureProvider
from runtime.science.experiment import Experiment, ExperimentProtocol
from runtime.science.peer_review import PeerReview
from runtime.science.publication import ScientificPaper
from runtime.science.knowledge_repository import KnowledgeRepository
from runtime.agents.agent import CognitiveAgent
from runtime.cogos.boot import CogOSBootloader

class MockScienceProvider:
    """
    Compliance test class for ScienceProvider Protocol interface.
    """
    def submit_hypothesis(self, concept_uri: str, hypothesis_data: dict) -> bool:
        return True

    def run_experiment(self, experiment_id: str) -> dict:
        return {"status": "simulated"}


class TestScientificMethod(unittest.TestCase):
    """
    TestScientificMethod validates PEP 544 interface declarations, experiment trial logic,
    peer replication voting, and concept promotion (Hypothesis -> Theory -> Law).
    """
    def test_protocol_compliance(self):
        # Assert type compliance on PEP 544 interfaces
        provider: ScienceProvider = MockScienceProvider()
        self.assertTrue(provider.submit_hypothesis("cse://concept/c1", {}))

    def test_experiment_execution(self):
        protocol = ExperimentProtocol(input_value=4.0, expected_output=16.0)
        experiment = Experiment("exp_test", protocol)

        # Successful exact execution Y = X * 4.0
        success, value = experiment.run_trial(lambda x: x * 4.0)
        self.assertTrue(success)
        self.assertAlmostEqual(value, 16.0)

        # Failed trial with wrong calculations
        success2, value2 = experiment.run_trial(lambda x: x * 3.0)
        self.assertFalse(success2)

    def test_peer_review_voting(self):
        reviewer = CognitiveAgent("Reviewer")
        protocol = ExperimentProtocol(input_value=5.0, expected_output=10.0)
        experiment = Experiment("exp_review", protocol)

        success, vote = PeerReview.verify_and_vote(reviewer, experiment, lambda x: x * 2.0)
        self.assertTrue(success)
        self.assertTrue(vote["agree"])
        self.assertEqual(vote["agent_id"], reviewer.identity.agent_id)

    def test_scientific_stage_upgrades(self):
        kernel = CogOSBootloader.boot()
        repo = KnowledgeRepository(kernel.system_state.knowledge_graph)
        concept_id = "cse://concept/relativity_test"

        kernel.system_state.knowledge_graph.add_node(concept_id, "RelativityTest", "Hypothesis")

        # Scenario 1: < 3 replications -> stays Hypothesis
        stage_1 = repo.audit_concept_maturity(concept_id, replication_count=2)
        self.assertEqual(stage_1, "HYPOTHESIS")

        # Scenario 2: >= 3 replications -> promotes to Theory
        stage_2 = repo.audit_concept_maturity(concept_id, replication_count=4)
        self.assertEqual(stage_2, "THEORY")

        # Scenario 3: >= 10 replications with low contradiction -> promotes to Law
        stage_3 = repo.audit_concept_maturity(concept_id, replication_count=11, contradiction_ratio=0.02)
        self.assertEqual(stage_3, "LAW")

        # Scenario 4: >= 10 replications with high contradiction -> demotes to Theory
        stage_4 = repo.audit_concept_maturity(concept_id, replication_count=12, contradiction_ratio=0.08)
        self.assertEqual(stage_4, "THEORY")

if __name__ == "__main__":
    unittest.main()
