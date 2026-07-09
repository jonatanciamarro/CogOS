import math
from runtime.observability.metric import Metric, MetricContext
from runtime.science.artifact import KnowledgeArtifact
from runtime.society.organization import OrganizationSnapshot, OrganizationStage


class CollectiveBureaucracyIndex:
    """
    CBI = coordination_cost / max(1.0, research_output)
    """
    name = "collective_bureaucracy_index"

    def compute(self, context: MetricContext) -> float:
        # Retrieve all institutions
        snapshots = []
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)

        total_coord_cost = 0.0
        # a * N^1.5 + b * log(N + 1)
        for org in snapshots:
            n = float(len(org.members))
            c_cost = (0.05 * (n ** 1.5)) + (0.05 * math.log1p(n))
            total_coord_cost += c_cost

        artifacts = [e for e in context.events if isinstance(e, KnowledgeArtifact)]
        research_output = float(len(artifacts))

        if research_output == 0.0:
            return total_coord_cost

        return total_coord_cost / research_output


class InstitutionalSweetSpot:
    """
    ISS = research_output / max(0.1, coordination_cost)
    """
    name = "institutional_sweet_spot"

    def compute(self, context: MetricContext) -> float:
        cbi_calc = CollectiveBureaucracyIndex()
        cbi = cbi_calc.compute(context)
        if cbi == 0.0:
            return 10.0
        return 1.0 / cbi


class AdaptiveResilienceScore:
    """
    ARS = post_crisis_output / max(0.1, pre_crisis_output)
    Determines performance retention after Black Swan shocks.
    """
    name = "adaptive_resilience_score"

    def compute(self, context: MetricContext) -> float:
        # Splits events before and after crisis tick (e.g. tick 100)
        crisis_tick = 100
        
        pre_crisis = 0
        post_crisis = 0
        
        for e in context.events:
            if isinstance(e, KnowledgeArtifact):
                if e.created_tick < crisis_tick:
                    pre_crisis += 1
                else:
                    post_crisis += 1

        if pre_crisis == 0:
            return 1.0
        return float(post_crisis) / pre_crisis


class KnowledgeRetentionTime:
    """
    KRT = average ticks from knowledge deprecation/loss to rediscovery.
    """
    name = "knowledge_retention_time"

    def compute(self, context: MetricContext) -> float:
        # Simple fallback representation for Sprint 5.2.1
        return 15.0
