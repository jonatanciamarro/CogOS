import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import ResourceType, KnowledgeArtifactType, TradeItem, AgentId, TradeStatus
from runtime.economy.utility_context import UtilityContext
from runtime.economy.utility_function import WeightedLogUtilityFunction
from runtime.economy.utility_policy import DeltaUtilityPolicy
from runtime.economy.decision_policy import WeightedDecisionPolicy, DecisionAction, DecisionEvaluation
from runtime.social.trade_proposal import TradeProposal
from runtime.economy.trade_history import TradeHistory
from runtime.social.matching_policy import ScarcityPolicy, RandomMatchingPolicy
from runtime.social.matching_engine import MatchingEngine, TradeOpportunity
from runtime.social.trade_engine import TradeEngine
from runtime.economy.resource_budget import ResourceBudget
from runtime.bus.event_bus import EventBus


class MockEnvironment:
    def scarcity(self, resource):
        return 0.5


class MockAgent:
    def __init__(self, agent_id: str, energy: float, attention: float = 20.0, knowledge: float = 0.0):
        self.identity = type("Identity", (object,), {"agent_id": AgentId(agent_id)})()
        self.resource_budget = ResourceBudget({"energy": energy, "attention": attention})
        self.knowledge = knowledge
        self.trust_score = 0.6

    def resource_amount(self, resource) -> float:
        if resource == ResourceType.ENERGY:
            return self.resource_budget.balances.get("energy", 0.0)
        if resource == ResourceType.ATTENTION:
            return self.resource_budget.balances.get("attention", 0.0)
        if resource == KnowledgeArtifactType.KNOWLEDGE:
            return self.knowledge
        return 0.0


class TestEmergentTradeLifecycle(unittest.TestCase):

    def test_trade_proposal_is_immutable(self):
        offer = (TradeItem(ResourceType.ENERGY, 10.0),)
        request = (TradeItem(ResourceType.ATTENTION, 5.0),)
        prop = TradeProposal(
            proposal_id="p1", parent_id=None,
            from_agent="a1", to_agent="a2",
            offer=offer, request=request,
            round=0, expires_tick=10,
            status=TradeStatus.PROPOSED
        )
        with self.assertRaises(Exception):
            prop.status = TradeStatus.ACCEPTED

    def test_trade_history_append_only_event_sourcing(self):
        hist = TradeHistory()
        offer = (TradeItem(ResourceType.ENERGY, 10.0),)
        request = (TradeItem(ResourceType.ATTENTION, 5.0),)
        prop = TradeProposal(
            proposal_id="p1", parent_id=None,
            from_agent="a1", to_agent="a2",
            offer=offer, request=request,
            round=0, expires_tick=10,
            status=TradeStatus.PROPOSED
        )

        hist.append("ProposalCreated", prop, 0.0)
        
        # Simulate counter proposal creation
        prop2 = TradeProposal(
            proposal_id="p2", parent_id="p1",
            from_agent="a2", to_agent="a1",
            offer=request, request=offer,
            round=1, expires_tick=10,
            status=TradeStatus.COUNTER
        )
        hist.append("CounterCreated", prop2, 1.0)

        events = hist.get_events()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_type, "ProposalCreated")
        self.assertEqual(events[1].event_type, "CounterCreated")

        # Verify chain reconstruction (P0 -> P1)
        chain = hist.get_chain("p2")
        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[0].proposal_id, "p1")
        self.assertEqual(chain[1].proposal_id, "p2")

    def test_matching_engine_scarcity_opportunities(self):
        engine = MatchingEngine(ScarcityPolicy())
        
        # A1 has excess energy, low attention
        a1 = MockAgent("a1", energy=1000.0, attention=5.0)
        # A2 has low energy, high attention
        a2 = MockAgent("a2", energy=100.0, attention=50.0)

        agents = {a1.identity.agent_id: a1, a2.identity.agent_id: a2}
        opps = engine.find_opportunities(agents, ctx=None)

        self.assertEqual(len(opps), 1)
        self.assertEqual(opps[0].from_agent_id, "a1")
        self.assertEqual(opps[0].to_agent_id, "a2")

    def test_trade_engine_negotiation_and_transactional_execution(self):
        bus = EventBus()
        engine = TradeEngine(event_bus=bus)

        a1 = MockAgent("a1", energy=200.0, attention=5.0)
        a2 = MockAgent("a2", energy=50.0, attention=50.0)

        offer = (TradeItem(ResourceType.ENERGY, 50.0),)
        request = (TradeItem(ResourceType.ATTENTION, 10.0),)

        # 1. Propose
        prop = engine.propose("a1", "a2", offer, request, tick=0)
        self.assertEqual(prop.status, TradeStatus.PROPOSED)

        # 2. Evaluate (Simulate acceptance)
        policy = WeightedDecisionPolicy()
        policy_util = DeltaUtilityPolicy()
        ctx = UtilityContext(current_tick=0, environment=MockEnvironment(), counterpart=a2)
        
        # Evaluate decision
        util_eval = policy_util.delta(a2, a2, ctx) # mock evaluation
        dec_eval = policy.evaluate_decision(util_eval, risk=0.0, exploration=0.0)
        dec_res = policy.decide(dec_eval) # w_util=1.0, score=0 -> ACCEPT

        resolved_prop = engine.evaluate_proposal(prop, dec_res, tick=1)
        self.assertEqual(resolved_prop.status, TradeStatus.ACCEPTED)

        # 3. Transactional Execute
        success = engine.commit_and_execute(resolved_prop, a1, a2, tick=2)
        self.assertTrue(success)

        # Verify resource balances transferred correctly
        self.assertEqual(a1.resource_budget.balances["energy"], 150.0)
        self.assertEqual(a2.resource_budget.balances["energy"], 100.0)
        self.assertEqual(a1.resource_budget.balances["attention"], 15.0)
        self.assertEqual(a2.resource_budget.balances["attention"], 40.0)

        # Verify Event Sourcing trail in history
        events = engine.history.get_events()
        self.assertEqual(events[-1].event_type, "Executed")
        self.assertEqual(events[-2].event_type, "Committed")

    def test_cb013a_two_agent_utility_exchange(self):
        """
        CB-013A: Two Agent Exchange.
        Verify that trading energy for knowledge increases net utility for both parts.
        """
        # A1: High energy (1000), low knowledge (1)
        a1 = MockAgent("a1", energy=1000.0, knowledge=1.0)
        # A2: Low energy (50), high knowledge (10)
        a2 = MockAgent("a2", energy=50.0, knowledge=10.0)

        func_a1 = WeightedLogUtilityFunction(w_energy=1.0, w_knowledge=3.0)
        func_a2 = WeightedLogUtilityFunction(w_energy=3.0, w_knowledge=1.0)

        policy_a1 = DeltaUtilityPolicy(func_a1)
        policy_a2 = DeltaUtilityPolicy(func_a2)

        ctx_a1 = UtilityContext(current_tick=0, environment=MockEnvironment(), counterpart=a2)
        ctx_a2 = UtilityContext(current_tick=0, environment=MockEnvironment(), counterpart=a1)

        # Before utilities
        u_a1_before = func_a1.evaluate(a1, ctx_a1)
        u_a2_before = func_a2.evaluate(a2, ctx_a2)

        # Simulate proposal trade: A1 offers 100 energy, requests 2 knowledge from B
        offer = (TradeItem(ResourceType.ENERGY, 100.0),)
        request = (TradeItem(KnowledgeArtifactType.KNOWLEDGE, 2.0),)

        # States AFTER trade if executed:
        a1_after = MockAgent("a1", energy=900.0, knowledge=3.0)
        a2_after = MockAgent("a2", energy=150.0, knowledge=8.0)

        # Evaluate transitions
        eval_a1 = policy_a1.delta(a1, a1_after, ctx_a1)
        eval_a2 = policy_a2.delta(a2, a2_after, ctx_a2)

        # Both should have delta > 0 (Pareto Efficient trade)
        self.assertGreater(eval_a1.delta, 0.0)
        self.assertGreater(eval_a2.delta, 0.0)

        # Net utility delta is positive
        self.assertGreater(eval_a1.delta + eval_a2.delta, 0.0)


if __name__ == "__main__":
    unittest.main()
