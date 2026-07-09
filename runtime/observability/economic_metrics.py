import math
from runtime.observability.metric import Metric, MetricContext, TradeMetricsEvent


class ParetoEfficiencyMetric:
    """
    PER = (trades where delta_a > 0 AND delta_b > 0) / total_executed_trades.
    """
    name = "pareto_efficiency_ratio"

    def compute(self, context: MetricContext) -> float:
        trade_events = [e for e in context.events if isinstance(e, TradeMetricsEvent)]
        if not trade_events:
            return 1.0  # Perfect efficiency when no wasteful trades occur

        efficient_trades = 0
        for e in trade_events:
            delta_a = e.utility_after_a - e.utility_before_a
            delta_b = e.utility_after_b - e.utility_before_b
            if delta_a > 0 and delta_b > 0:
                efficient_trades += 1

        return float(efficient_trades) / len(trade_events)


class TradeAcceptanceMetric:
    """
    TAR = accepted_trades / total_proposals.
    Scans the events list for proposed and accepted states.
    """
    name = "trade_acceptance_ratio"

    def compute(self, context: MetricContext) -> float:
        # We can extract proposals and accepted statuses from event history
        proposals = 0
        accepts = 0
        for e in context.events:
            # We check proposals from event log or EventBus events
            if hasattr(e, "status"):
                from runtime.economy.types import TradeStatus
                if e.status == TradeStatus.PROPOSED:
                    proposals += 1
                elif e.status == TradeStatus.ACCEPTED:
                    accepts += 1

        if proposals == 0:
            return 0.0
        return float(accepts) / proposals


class NegotiationDepthMetric:
    """
    ND = sum(negotiation_rounds) / total_executed_trades.
    """
    name = "negotiation_depth"

    def compute(self, context: MetricContext) -> float:
        trade_events = [e for e in context.events if isinstance(e, TradeMetricsEvent)]
        if not trade_events:
            return 0.0

        total_rounds = sum(e.negotiation_depth for e in trade_events)
        return float(total_rounds) / len(trade_events)


class ValueCreationMetric:
    """
    VCR = sum(delta_a + delta_b) / max(1, total_resources_transferred).
    """
    name = "value_creation_ratio"

    def compute(self, context: MetricContext) -> float:
        trade_events = [e for e in context.events if isinstance(e, TradeMetricsEvent)]
        if not trade_events:
            return 0.0

        total_utility_delta = 0.0
        total_resources = 0.0

        for e in trade_events:
            delta_a = e.utility_after_a - e.utility_before_a
            delta_b = e.utility_after_b - e.utility_before_b
            total_utility_delta += (delta_a + delta_b)
            total_resources += e.resources_transferred

        if total_resources == 0.0:
            return 0.0
        return total_utility_delta / total_resources


class AverageCreatedValueMetric:
    """
    ACV = sum(delta_a + delta_b) / total_executed_trades.
    """
    name = "average_created_value"

    def compute(self, context: MetricContext) -> float:
        trade_events = [e for e in context.events if isinstance(e, TradeMetricsEvent)]
        if not trade_events:
            return 0.0

        total_utility_delta = 0.0
        for e in trade_events:
            delta_a = e.utility_after_a - e.utility_before_a
            delta_b = e.utility_after_b - e.utility_before_b
            total_utility_delta += (delta_a + delta_b)

        return total_utility_delta / len(trade_events)


class EconomicIndexMetric:
    """
    Aggregated Economic index metric contributing to the CCI score.
    Fuses Pareto Efficiency and Average Created Value:
    EconomicIndex = PER * log1p(ACV * total_trades)
    """
    name = "economic_index"

    def __init__(self):
        self.per = ParetoEfficiencyMetric()
        self.acv = AverageCreatedValueMetric()

    def compute(self, context: MetricContext) -> float:
        per_score = self.per.compute(context)
        acv_score = self.acv.compute(context)
        trade_events = [e for e in context.events if isinstance(e, TradeMetricsEvent)]
        
        # Scale logarithmically based on active commerce volume
        volume_factor = math.log1p(acv_score * len(trade_events))
        return min(1.0, per_score * volume_factor)


class KnowledgeIndexMetric:
    """
    Simple placeholder knowledge index for Sprint 5.1.
    """
    name = "knowledge_index"

    def compute(self, context: MetricContext) -> float:
        # Standard default score for Sprint 5.1
        return 0.1
