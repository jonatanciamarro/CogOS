from dataclasses import dataclass
from runtime.economy.types import AgentId
from runtime.science.artifact_stage import ArtifactStage


@dataclass(frozen=True)
class KnowledgeArtifact:
    """
    An immutable scientific artifact representing a node in the civilization knowledge graph.
    Trackable lineage via parent_artifact_id and contributors.
    """
    artifact_id:        str
    title:              str
    stage:              ArtifactStage
    confidence:         float
    replications:       int
    contradictions:     int
    novelty:            float
    author:             AgentId
    parent_artifact_id: str | None
    contributors:       tuple[AgentId, ...]
    created_tick:       int
    accessibility:      float = 1.0
    niche:              str = "general"
    origin_species:     str | None = None



    @property
    def contradiction_ratio(self) -> float:
        total = self.replications + self.contradictions
        if total == 0:
            return 0.0
        return float(self.contradictions) / total
