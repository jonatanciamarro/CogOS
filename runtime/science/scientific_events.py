from dataclasses import dataclass
from runtime.economy.types import AgentId
from runtime.science.artifact_stage import ArtifactStage


@dataclass(frozen=True)
class ArtifactPromotedEvent:
    """Fired when an artifact matures to a higher stage."""
    artifact_id:    str
    previous_stage: ArtifactStage
    new_stage:      ArtifactStage
    timestamp:      float


@dataclass(frozen=True)
class ArtifactReviewedEvent:
    """Fired when a peer review is registered."""
    artifact_id:      str
    reviewer:         AgentId
    confidence_delta: float
    timestamp:        float


@dataclass(frozen=True)
class ArtifactReplicatedEvent:
    """Fired when a replication trial is conducted."""
    artifact_id: str
    replicator:  AgentId
    success:     bool
    timestamp:   float


@dataclass(frozen=True)
class ArtifactRejectedEvent:
    """Fired when an artifact fails validation and gets rejected."""
    artifact_id: str
    reason:      str
    timestamp:   float


@dataclass(frozen=True)
class ArtifactDeprecatedEvent:
    """Fired when a technology becomes obsolete or deprecated."""
    artifact_id: str
    reason:      str
    timestamp:   float
