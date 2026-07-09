from typing import Any
from runtime.observability.metric import Metric, MetricContext
from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_stage import ArtifactStage
from runtime.society.organization import OrganizationSnapshot, OrganizationStage


class ResearchCollaborationRate:
    """
    RCR = collaborative_research (contributors >= 2) / total_research.
    """
    name = "research_collaboration_rate"

    def compute(self, context: MetricContext) -> float:
        artifacts = [e for e in context.events if isinstance(e, KnowledgeArtifact)]
        if not artifacts:
            return 0.0

        collaborative = sum(1 for art in artifacts if len(art.contributors) >= 2)
        return float(collaborative) / len(artifacts)


class DiscoveryVelocity:
    """
    DV = (new_artifacts * KQI) / (agent_count * ticks).
    """
    name = "discovery_velocity"

    def compute(self, context: MetricContext) -> float:
        artifacts = [e for e in context.events if isinstance(e, KnowledgeArtifact)]
        if not artifacts:
            return 0.0

        agent_count = 100 # default baseline for normalized comparisons
        ticks = max(1, context.tick)

        kqi_calc = KnowledgeQualityIndex()
        kqi = kqi_calc.compute(context)

        return (len(artifacts) * kqi) / (agent_count * ticks)


class KnowledgeTransferEfficiency:
    """
    KTE = agents receiving validated knowledge / total_agents.
    """
    name = "knowledge_transfer_efficiency"

    def compute(self, context: MetricContext) -> float:
        # Check event log for KnowledgeSharedEvent or similar
        # Fallback to general ratio of agents holding theories
        total_agents = 100.0
        shared_count = 0
        
        # Look for custom shared event or read from world snapshot
        for event in context.events:
            if hasattr(event, "event_type") and event.event_type == "KnowledgeSharedEvent":
                shared_count += 1
                
        return min(1.0, float(shared_count) / total_agents)


class InstitutionFormationRate:
    """
    IFR = stable_organizations / ticks.
    """
    name = "institution_formation_rate"

    def compute(self, context: MetricContext) -> float:
        ticks = max(1, context.tick)
        stable_count = 0

        # Organizations are stable if active/specialized and survived > 5 ticks
        snapshots = []
        # Fallback query from world snapshot if available
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)

        for snap in snapshots:
            if snap.stage in (OrganizationStage.ACTIVE, OrganizationStage.SPECIALIZED):
                age = ticks - snap.created_tick
                if age >= 5:
                    stable_count += 1

        return float(stable_count) / ticks


class InstitutionSurvivalRate:
    """
    ISR = surviving_organizations / created_organizations.
    """
    name = "institution_survival_rate"

    def compute(self, context: MetricContext) -> float:
        created = 0
        surviving = 0

        for event in context.events:
            if hasattr(event, "event_type") or hasattr(event, "__class__"):
                name = getattr(event, "event_type", event.__class__.__name__)
                if "OrganizationCreated" in name:
                    created += 1
                elif "OrganizationCollapsed" in name:
                    pass

        # Query active from world
        snapshots = []
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)

        surviving = sum(1 for snap in snapshots if snap.stage != OrganizationStage.COLLAPSED)
        
        if created == 0:
            return 1.0
        return float(surviving) / created


class KnowledgeQualityIndex:
    """
    KQI = (validated_theories / total_theories) * average_confidence * average_novelty.
    """
    name = "knowledge_quality_index"

    def compute(self, context: MetricContext) -> float:
        artifacts = [e for e in context.events if isinstance(e, KnowledgeArtifact)]
        if not artifacts:
            return 1.0

        validated = sum(1 for art in artifacts if art.stage in (ArtifactStage.THEORY, ArtifactStage.TECHNOLOGY))
        validation_ratio = float(validated) / len(artifacts) if validated > 0 else 0.1

        avg_conf = sum(art.confidence for art in artifacts) / len(artifacts)
        avg_nov  = sum(art.novelty for art in artifacts) / len(artifacts)

        return validation_ratio * avg_conf * avg_nov
