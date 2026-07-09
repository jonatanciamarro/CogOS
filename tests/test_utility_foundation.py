import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import ResourceType, KnowledgeArtifactType, TradeItem, AgentId
from runtime.economy.utility_context import UtilityContext
from runtime.economy.utility_function import WeightedLogUtilityFunction
from runtime.economy.utility_policy import DeltaUtilityPolicy, UtilityComponent
from runtime.economy.decision_policy import WeightedDecisionPolicy, DecisionFactor, DecisionEvaluation, DecisionAction



class MockEnvironment:
    def scarcity(self, resource):
        return 0.5


class MockAgent:
    def __init__(self, agent_id: str, energy: float, knowledge: float, trust: float = 0.5):
        self._id = AgentId(agent_id)
        self.energy = energy
        self.knowledge = knowledge
        self.trust_score = trust

    @property
    def id(self) -> AgentId:
        return self._id

    def resource_amount(self, resource) -> float:
        if resource == ResourceType.ENERGY:
            return self.energy
        if resource == KnowledgeArtifactType.KNOWLEDGE:
            return self.knowledge
        return 0.0


class TestUtilityFoundation(unittest.TestCase):

    def test_trade_item_is_hashable_and_immutable(self):
        item = TradeItem(
            ResourceType.ENERGY,
            10.0,
            metadata=(("source", "agent_a"), ("priority", "high"))
        )
        # Verify hashability
        self.assertIsNotNone(hash(item))

        # Verify immutability (frozen=True raises exception on write)
        with self.assertRaises(Exception):
            item.amount = 20.0

    def test_utility_function_is_deterministic_and_pure(self):
        func = WeightedLogUtilityFunction(w_energy=1.5, w_knowledge=0.8, w_trust=2.0)
        agent = MockAgent("agent_1", energy=100.0, knowledge=16.0, trust=0.8)
        ctx = UtilityContext(
            current_tick=42,
            environment=MockEnvironment(),
            counterpart=MockAgent("agent_2", energy=50.0, knowledge=4.0)
        )

        # Get multiple evaluations
        u1 = func.evaluate(agent, ctx)
        u2 = func.evaluate(agent, ctx)

        # 1. Determinism
        self.assertEqual(u1, u2)

        # 2. Pureness: Verify state has not changed
        self.assertEqual(agent.energy, 100.0)
        self.assertEqual(agent.knowledge, 16.0)
        self.assertEqual(agent.trust_score, 0.8)

    def test_delta_utility_policy(self):
        policy = DeltaUtilityPolicy(WeightedLogUtilityFunction(w_energy=1.0, w_knowledge=1.0, w_trust=0.0))
        before = MockAgent("agent_1", energy=10.0, knowledge=4.0)
        after  = MockAgent("agent_1", energy=20.0, knowledge=9.0)
        ctx = UtilityContext(current_tick=0, environment=MockEnvironment(), counterpart=MockAgent("agent_2", energy=0, knowledge=0))

        eval_res = policy.delta(before, after, ctx)

        # before: log(11) + sqrt(4) = 2.397895 + 2 = 4.397895
        # after: log(21) + sqrt(9) = 3.044522 + 3 = 6.044522
        self.assertAlmostEqual(eval_res.before, 4.397895, places=5)
        self.assertAlmostEqual(eval_res.after, 6.044522, places=5)
        self.assertAlmostEqual(eval_res.delta, 1.646627, places=5)
        self.assertEqual(eval_res.confidence, 1.0)
        self.assertIn(UtilityComponent.ENERGY, eval_res.components)

    def test_weighted_decision_policy(self):
        policy = WeightedDecisionPolicy(w_util=1.0, w_risk=-1.0, w_exp=0.5, accept_threshold=0.0, defer_threshold=-0.5)
        policy_util = DeltaUtilityPolicy(WeightedLogUtilityFunction(w_energy=1.0, w_knowledge=1.0, w_trust=0.0))
        before = MockAgent("agent_1", energy=10.0, knowledge=4.0)
        after  = MockAgent("agent_1", energy=20.0, knowledge=9.0)
        ctx = UtilityContext(current_tick=0, environment=MockEnvironment(), counterpart=MockAgent("agent_2", energy=0, knowledge=0))

        utility_eval = policy_util.delta(before, after, ctx)
        dec_eval = policy.evaluate_decision(utility_eval, risk=0.2, exploration=0.1)

        # score = 1.646627 * 1.0 + 0.2 * (-1.0) + 0.1 * 0.5 = 1.646627 - 0.2 + 0.05 = 1.496627
        self.assertAlmostEqual(dec_eval.score, 1.496627, places=5)

        dec_result = policy.decide(dec_eval)
        self.assertEqual(dec_result.action, DecisionAction.ACCEPT)
        self.assertEqual(dec_result.dominant_factor, DecisionFactor.UTILITY)
        self.assertGreater(dec_result.decision_latency, 0.0)



if __name__ == "__main__":
    unittest.main()
