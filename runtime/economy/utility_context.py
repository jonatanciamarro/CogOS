from dataclasses import dataclass
from typing import Protocol, Any, runtime_checkable
from runtime.economy.types import AgentId, ResourceType, KnowledgeArtifactType


@runtime_checkable
class EnvironmentView(Protocol):
    """
    Decoupled view of the environment.
    Allows UtilityPolicies to query scarcity or environmental states.
    """
    def scarcity(self, resource: ResourceType | KnowledgeArtifactType) -> float:
        ...


@runtime_checkable
class AgentSnapshot(Protocol):
    """
    Decoupled snapshot of a counterpart agent participating in a trade.
    """
    @property
    def id(self) -> AgentId:
        ...

    def resource_amount(self, resource: ResourceType | KnowledgeArtifactType) -> float:
        ...


@dataclass(frozen=True)
class UtilityContext:
    """
    Immutable context passed to utility functions and policies.
    Guarantees that evaluation depends only on explicit, testable parameters.
    """
    current_tick: int
    environment: EnvironmentView
    counterpart: AgentSnapshot
