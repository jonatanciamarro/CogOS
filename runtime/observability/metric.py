from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any
from runtime.economy.types import TradeId


@dataclass(frozen=True)
class TradeMetricsEvent:
    """
    Decoupled event carrying performance and utility metrics for completed trades.
    Published by TradeEngine, consumed by Telemetry and MetricRegistry.
    """
    trade_id:             TradeId
    utility_before_a:     float
    utility_after_a:      float
    utility_before_b:     float
    utility_after_b:      float
    resources_transferred: float
    negotiation_depth:    int


@dataclass(frozen=True)
class MetricContext:
    """
    Immutable context passed to metric calculation engines.
    """
    tick:           int
    events:         tuple[Any, ...]
    world_snapshot: Any


@runtime_checkable
class Metric(Protocol):
    """
    PEP 544 Protocol for modular indicators contributing to the CCI.
    """
    name: str

    def compute(self, context: MetricContext) -> float:
        ...
