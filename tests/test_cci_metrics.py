import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import ResourceType, TradeStatus, ProposalId
from runtime.social.trade_proposal import TradeProposal
from runtime.observability.metric import TradeMetricsEvent, MetricContext
from runtime.observability.metrics_registry import MetricRegistry, CCICalculator
from runtime.observability.economic_metrics import (
    ParetoEfficiencyMetric, TradeAcceptanceMetric, NegotiationDepthMetric,
    ValueCreationMetric, AverageCreatedValueMetric, EconomicIndexMetric, KnowledgeIndexMetric
)


class TestCCIMetrics(unittest.TestCase):

    def test_pareto_efficiency_metric(self):
        metric = ParetoEfficiencyMetric()
        
        # 1. Test empty events
        ctx_empty = MetricContext(tick=0, events=(), world_snapshot=None)
        self.assertEqual(metric.compute(ctx_empty), 1.0)

        # 2. Mix of efficient and inefficient trades
        # Event 1: Pareto efficient (both delta > 0)
        e1 = TradeMetricsEvent(
            trade_id="t1",
            utility_before_a=1.0, utility_after_a=1.5, # delta = 0.5
            utility_before_b=2.0, utility_after_b=2.1, # delta = 0.1
            resources_transferred=10.0, negotiation_depth=0
        )
        # Event 2: Inefficient (one delta is negative)
        e2 = TradeMetricsEvent(
            trade_id="t2",
            utility_before_a=1.0, utility_after_a=0.9, # delta = -0.1
            utility_before_b=2.0, utility_after_b=2.5, # delta = 0.5
            resources_transferred=20.0, negotiation_depth=1
        )
        ctx = MetricContext(tick=0, events=(e1, e2), world_snapshot=None)
        self.assertEqual(metric.compute(ctx), 0.5)

    def test_trade_acceptance_ratio(self):
        metric = TradeAcceptanceMetric()

        # Simulate proposals in events history
        p1 = TradeProposal("p1", None, "a1", "a2", (), (), 0, 10, TradeStatus.PROPOSED)
        p2 = TradeProposal("p2", None, "a2", "a1", (), (), 0, 10, TradeStatus.ACCEPTED)
        p3 = TradeProposal("p3", None, "a1", "a2", (), (), 0, 10, TradeStatus.PROPOSED)

        ctx = MetricContext(tick=0, events=(p1, p2, p3), world_snapshot=None)
        # TAR = 1 accepted / 2 proposed = 0.5
        self.assertEqual(metric.compute(ctx), 0.5)

    def test_negotiation_depth(self):
        metric = NegotiationDepthMetric()
        e1 = TradeMetricsEvent("t1", 0, 1, 0, 1, 10.0, negotiation_depth=2)
        e2 = TradeMetricsEvent("t2", 0, 1, 0, 1, 10.0, negotiation_depth=0)
        ctx = MetricContext(tick=0, events=(e1, e2), world_snapshot=None)
        # Average rounds = (2 + 0) / 2 = 1.0
        self.assertEqual(metric.compute(ctx), 1.0)

    def test_value_creation_ratio_and_acv(self):
        vcr = ValueCreationMetric()
        acv = AverageCreatedValueMetric()

        e1 = TradeMetricsEvent("t1", 1.0, 1.5, 2.0, 2.1, resources_transferred=10.0, negotiation_depth=0) # delta_sum = 0.6
        e2 = TradeMetricsEvent("t2", 1.0, 2.0, 2.0, 2.4, resources_transferred=20.0, negotiation_depth=0) # delta_sum = 1.4

        ctx = MetricContext(tick=0, events=(e1, e2), world_snapshot=None)

        # VCR = (0.6 + 1.4) / (10 + 20) = 2.0 / 30.0 = 0.06666...
        self.assertAlmostEqual(vcr.compute(ctx), 0.06666667, places=5)
        # ACV = 2.0 / 2 = 1.0
        self.assertEqual(acv.compute(ctx), 1.0)

    def test_metric_registry_and_cci_calculator(self):
        registry = MetricRegistry()
        registry.register_metric(EconomicIndexMetric())
        registry.register_metric(KnowledgeIndexMetric())

        # Log some events in registry
        p1 = TradeProposal("p1", None, "a1", "a2", (), (), 0, 10, TradeStatus.PROPOSED)
        e1 = TradeMetricsEvent("t1", 1.0, 2.0, 2.0, 3.0, resources_transferred=10.0, negotiation_depth=1) # delta = 1+1 = 2
        registry.log_event(p1)
        registry.log_event(e1)

        calculator = CCICalculator(registry, weights={"economic_index": 0.8, "knowledge_index": 0.2})
        cci = calculator.calculate_cci(tick=10, world_snapshot=None)

        # PER = 1.0, ACV = 2.0, len = 1
        # EconomicIndex = 1.0 * log1p(2.0 * 1) = log(3) = 1.0986... -> capped at 1.0
        # KnowledgeIndex = 0.1
        # CCI = 0.8 * 1.0 + 0.2 * 0.1 = 0.8 + 0.02 = 0.82
        self.assertAlmostEqual(cci, 0.82, places=4)


if __name__ == "__main__":
    unittest.main()
