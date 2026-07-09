from typing import Any
from runtime.observability.metric import Metric, MetricContext


class MetricRegistry:
    """
    MetricRegistry holds all registered Metric indicators.
    It collects push-based simulation events reactively and passes them
    in a clean MetricContext during evaluation intervals.
    """
    def __init__(self):
        self._metrics: dict[str, Metric] = {}
        self._events_buffer: list[Any] = []

    def register_metric(self, metric: Metric) -> None:
        """Registers a new metric tracker."""
        self._metrics[metric.name] = metric

    def get_metric(self, name: str) -> Metric | None:
        return self._metrics.get(name)

    def log_event(self, event: Any) -> None:
        """Push-based event logging."""
        self._events_buffer.append(event)

    def clear_events(self) -> None:
        self._events_buffer.clear()

    def compute_all(self, tick: int, world_snapshot: Any) -> dict[str, float]:
        """
        Computes all registered metrics under a single context view.
        """
        ctx = MetricContext(
            tick=tick,
            events=tuple(self._events_buffer),
            world_snapshot=world_snapshot
        )
        return {name: metric.compute(ctx) for name, metric in self._metrics.items()}

    def registered_metric_names(self) -> list[str]:
        return list(self._metrics.keys())


class CCICalculator:
    """
    Aggregates sub-metrics into the Civilization Complexity Index (CCI).
    Decoupled: registry logs push events, CCI queries compute_all().
    """
    def __init__(self, registry: MetricRegistry, weights: dict[str, float] = None):
        self.registry = registry
        # Default weights for Sprint 5.1
        self.weights = weights or {
            "economic_index": 0.5,
            "knowledge_index": 0.5
        }

    def calculate_cci(self, tick: int, world_snapshot: Any) -> float:
        """
        Calculates the aggregated CCI score.
        """
        values = self.registry.compute_all(tick, world_snapshot)
        total = 0.0
        weight_sum = sum(self.weights.values()) or 1.0

        for name, weight in self.weights.items():
            total += weight * values.get(name, 0.0)

        return total / weight_sum
