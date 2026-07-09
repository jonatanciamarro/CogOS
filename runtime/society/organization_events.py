from dataclasses import dataclass
from runtime.economy.types import AgentId
from runtime.science.artifact import KnowledgeArtifact


@dataclass(frozen=True)
class OrganizationCreatedEvent:
    org_id:       str
    name:         str
    mission:      str
    creator:      AgentId
    created_tick: int
    timestamp:    float


@dataclass(frozen=True)
class MemberJoinedEvent:
    org_id:     str
    member_id:  AgentId
    timestamp:  float


@dataclass(frozen=True)
class MemberLeftEvent:
    org_id:     str
    member_id:  AgentId
    timestamp:  float


@dataclass(frozen=True)
class BudgetAllocatedEvent:
    org_id:        str
    resource_type: str
    amount:        float
    timestamp:     float


@dataclass(frozen=True)
class TechnologyProducedEvent:
    org_id:      str
    artifact_id: str
    timestamp:   float


@dataclass(frozen=True)
class OrganizationCollapsedEvent:
    org_id:    str
    reason:    str
    timestamp: float


@dataclass(frozen=True)
class OrganizationSpecializedEvent:
    org_id:          str
    specializations: tuple[str, ...]
    timestamp:       float


@dataclass(frozen=True)
class ResearchStartedEvent:
    org_id:      str
    artifact_id: str
    timestamp:   float


@dataclass(frozen=True)
class ResearchCompletedEvent:
    org_id:      str
    artifact_id: str
    success:     bool
    timestamp:   float


@dataclass(frozen=True)
class SpeciationEvent:
    org_id:      str
    old_profile: str
    new_profile: str
    timestamp:   float


@dataclass(frozen=True)
class AdaptationEvent:
    org_id:         str
    fitness_before: float
    fitness_after:  float
    trigger:        str
    timestamp:      float


@dataclass(frozen=True)
class ExtinctionEvent:
    org_id:           str
    name:             str
    profile:          str
    lineage_depth:    int
    artifacts_count:  int
    timestamp:        float

