"""
runtime/contracts/__init__.py

ISP-style PEP 544 Protocols for CogOS.
Each interface is intentionally small — classes satisfy them implicitly via structural subtyping.
Sprint 5.X adds new protocols without touching existing ones.
"""
from typing import Protocol, runtime_checkable, Any


# ─── Agent-level capability interfaces ─────────────────────────────────────

@runtime_checkable
class IdentityProvider(Protocol):
    """Any entity that has a stable identity object."""
    identity: Any


@runtime_checkable
class BudgetProvider(Protocol):
    """Any entity that owns a ResourceBudget."""
    resource_budget: Any


@runtime_checkable
class TrustProvider(Protocol):
    """Any entity tracked by the trust/reputation system."""
    trust_score: float
    historical_efficiency: float


@runtime_checkable
class TaskExecutable(Protocol):
    """A callable unit of work."""
    id: str
    agent_id: str
    cost_estimate: int
    urgency: float
    expected_information_gain: float
    def __call__(self) -> None: ...


@runtime_checkable
class Observable(Protocol):
    """Any entity that perceives the Environment."""
    def observe(self, environment: Any) -> None: ...


@runtime_checkable
class HistoricalEntity(Protocol):
    """Any entity whose events can be logged to CivilizationMemory."""
    def record_event(self, event: Any) -> None: ...


# ─── Subsystem protocols ────────────────────────────────────────────────────

@runtime_checkable
class SchedulerProtocol(Protocol):
    def rank_tasks(self, tasks: list, agents_by_id: dict) -> list: ...
    def allocate_cpu_slice(self, agents: list, total_cpu: int) -> dict: ...


@runtime_checkable
class EventBusProtocol(Protocol):
    def subscribe(self, event_type: str, handler: Any, priority: Any = None) -> None: ...
    def publish(self, event_type: str, payload: Any, priority: Any = None) -> int: ...
    def publish_sync(self, event_type: str, payload: Any, priority: Any = None) -> int: ...
    def publish_async(self, event_type: str, payload: Any, priority: Any = None) -> Any: ...



@runtime_checkable
class BudgetProtocol(Protocol):
    def consume(self, dimension: str, amount: int) -> Any: ...
    def replenish(self, dimension: str, amount: int) -> None: ...


@runtime_checkable
class ScienceProtocol(Protocol):
    def submit_experiment(self, experiment: Any) -> Any: ...
    def peer_review(self, paper_id: str) -> Any: ...


@runtime_checkable
class CultureProtocol(Protocol):
    def propagate_meme(self, meme: Any, population: list) -> None: ...
    def cultural_selection(self) -> None: ...


@runtime_checkable
class HistoryProtocol(Protocol):
    def log_event(self, event: Any) -> None: ...
    def current_epoch(self) -> int: ...


@runtime_checkable
class EconomyProtocol(Protocol):
    def rank_by_evi(self) -> list: ...
    def invest(self, hypothesis_id: str, agent_budget: Any, amount: int) -> bool: ...


@runtime_checkable
class TelemetryProtocol(Protocol):
    def on_event(self, event_type: str, payload: Any) -> None: ...
    def snapshot(self) -> dict: ...


@runtime_checkable
class EnvironmentSystem(Protocol):
    """A pluggable system that evolves the Environment each tick."""
    name: str
    def tick(self, context: Any) -> None: ...
