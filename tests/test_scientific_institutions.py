import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage
from runtime.society.organization_utility import OrganizationUtilityFunction
from runtime.observability.metric import MetricContext
from runtime.observability.scientific_metrics import DiscoveryVelocity, KnowledgeQualityIndex
from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_stage import ArtifactStage
from runtime.economy.resource_budget import ResourceBudget


class TestScientificInstitutions(unittest.TestCase):

    def test_kqi_is_deterministic_and_valid(self):
        kqi_calc = KnowledgeQualityIndex()
        
        art1 = KnowledgeArtifact("art-1", "A", ArtifactStage.THEORY, 0.8, 5, 0, 0.9, AgentId("a"), None, (), 1)
        art2 = KnowledgeArtifact("art-2", "B", ArtifactStage.IDEA, 0.4, 0, 0, 0.6, AgentId("b"), None, (), 1)
        
        ctx = MetricContext(tick=10, events=(art1, art2), world_snapshot=None)
        
        # Multiple runs must yield exact same result
        kqi1 = kqi_calc.compute(ctx)
        kqi2 = kqi_calc.compute(ctx)
        
        self.assertEqual(kqi1, kqi2)
        # Validation ratio is 0.5 (1 of 2 is THEORY), conf = 0.6, novelty = 0.75 -> positive index
        self.assertGreater(kqi1, 0.0)

    def test_coordination_cost_triggers_collapse_or_leave(self):
        utility_func = OrganizationUtilityFunction(coordination_weight=2.0, autonomy_loss=1.0)
        
        # Org with extremely high member count (50 members) under high coordination weight
        org = OrganizationSnapshot(
            org_id="org-heavy", name="Huge Lab", mission="general", specialization=(), stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(50)), reputation=1.0,
            resources=ResourceBudget({"energy": 100, "attention": 10}), collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0
        )
        
        solo_utility = 5.0
        # The coordination cost of 50 members * 2.0 = 100.0 coordination penalty makes the join score highly negative!
        score = utility_func.evaluate_join_score("agent-x", org, solo_utility)
        
        # Score is heavily negative, triggering members to leave or collapse
        self.assertLess(score, -5.0)

    def test_institutions_increase_discovery_velocity(self):
        dv_calc = DiscoveryVelocity()
        
        # Scenario A: Solo agents (1 discovery)
        art1 = KnowledgeArtifact("art-1", "A", ArtifactStage.THEORY, 0.8, 5, 0, 0.9, AgentId("a"), None, (), 1)
        ctx_solo = MetricContext(tick=100, events=(art1,), world_snapshot=None)
        dv_solo = dv_calc.compute(ctx_solo)

        # Scenario B: Institutional pooling (10 discoveries)
        arts_coop = [
            KnowledgeArtifact(f"art-{i}", "A", ArtifactStage.THEORY, 0.8, 5, 0, 0.9, AgentId("a"), None, (), 1)
            for i in range(10)
        ]
        ctx_coop = MetricContext(tick=100, events=tuple(arts_coop), world_snapshot=None)
        dv_coop = dv_calc.compute(ctx_coop)

        self.assertGreater(dv_coop, dv_solo)


if __name__ == "__main__":
    unittest.main()
