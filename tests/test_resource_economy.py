import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.budget_policy import BudgetPolicy
from runtime.economy.resource_budget import ResourceBudget, BudgetResult
from runtime.economy.credit_economy import CreditLedger
from runtime.economy.scheduling_policy import GreedyPolicy, ScientificPolicy
from runtime.economy.market import IdeaMarket
from runtime.bus.event_bus import EventBus, EventPriority, CogOSEvents
from runtime.execution.task_queue import Task, TaskQueue
from runtime.execution.rollback import RollbackManager
from runtime.agents.agent import CognitiveAgent

class TestResourceEconomy(unittest.TestCase):

    def test_budget_policy_presets(self):
        founder  = BudgetPolicy.for_role("founder")
        standard = BudgetPolicy.for_role("standard")
        self.assertGreater(founder["cpu"], standard["cpu"])
        self.assertGreater(founder["memory"], standard["memory"])

    def test_budget_result_structured(self):
        budget = ResourceBudget(BudgetPolicy.STANDARD)
        result = budget.consume("cpu", 100)
        self.assertTrue(result.ok)
        self.assertEqual(result.status, "OK")

        result2 = budget.consume("cpu", 99999)
        self.assertFalse(result2.ok)
        self.assertEqual(result2.status, "INSUFFICIENT_CPU")
        self.assertGreater(result2.deficit, 0)

    def test_budget_exhaustion_no_panic(self):
        budget = ResourceBudget({"cpu": 5})
        result = budget.consume("cpu", 1000)
        self.assertFalse(result.ok)
        # No exception raised — silent fail confirmed

    def test_credit_accumulation_via_events(self):
        ledger = CreditLedger()
        ledger.award(CogOSEvents.PUBLICATION_ACCEPTED)
        self.assertEqual(ledger.balances["scientific_credits"], 20)
        ledger.award(CogOSEvents.PEER_REVIEW_PASSED)
        self.assertEqual(ledger.balances["trust_credits"], 10)

    def test_scheduler_utility_formula(self):
        from runtime.execution.task_queue import Task
        t1 = Task("t1", "a1", lambda: None, priority=10, cost_estimate=2,
                  urgency=0.9, expected_information_gain=0.8)
        t2 = Task("t2", "a2", lambda: None, priority=1,  cost_estimate=10,
                  urgency=0.1, expected_information_gain=0.1)

        class MockAgent:
            historical_efficiency = 0.9
            trust_score = 0.8

        policy = GreedyPolicy()
        s1 = policy.score(t1, MockAgent())
        s2 = policy.score(t2, MockAgent())
        self.assertGreater(s1, s2)

    def test_eventbus_priority_ordering(self):
        bus = EventBus()
        order = []
        bus.subscribe("EVT", lambda e, p: order.append("HIGH"),   EventPriority.HIGH)
        bus.subscribe("EVT", lambda e, p: order.append("LOW"),    EventPriority.LOW)
        bus.subscribe("EVT", lambda e, p: order.append("CRITICAL"), EventPriority.CRITICAL)
        bus.publish("EVT", {})
        self.assertEqual(order, ["CRITICAL", "HIGH", "LOW"])

    def test_rollback_delta_diff(self):
        agent = CognitiveAgent("TestAgent")
        rb = RollbackManager()

        rb.checkpoint(agent)
        original_phase = agent.cognitive_phase

        from runtime.agents.cognitive_phase import CognitivePhase
        agent.cognitive_phase = CognitivePhase.REFLECT

        rb.checkpoint(agent)
        rb.restore(agent)

        self.assertEqual(agent.cognitive_phase, original_phase)


if __name__ == "__main__":
    unittest.main()
