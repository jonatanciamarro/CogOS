import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.science.artifact_stage import ArtifactStage
from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_lifecycle import promote_artifact, replicate_artifact, review_artifact
from runtime.science.peer_review import ReputationPeerReviewer
from runtime.science.knowledge_repository import KnowledgeRepository
from runtime.science.knowledge_value import KnowledgeValueFunction


class TestKnowledgeEconomy(unittest.TestCase):

    def test_complete_knowledge_transition_lifecycle(self):
        # 1. Start with an Idea
        art = KnowledgeArtifact(
            artifact_id="art-001",
            title="Dark Energy Theory",
            stage=ArtifactStage.IDEA,
            confidence=0.5,
            replications=0,
            contradictions=0,
            novelty=0.9,
            author=AgentId("agent-a"),
            parent_artifact_id=None,
            contributors=(AgentId("agent-a"),),
            created_tick=1
        )
        self.assertEqual(art.stage, ArtifactStage.IDEA)

        # Promote fails since confidence <= 0.6
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.IDEA)

        # 2. Peer Review boosts confidence
        art = review_artifact(art, confidence_delta=0.2)
        self.assertAlmostEqual(art.confidence, 0.7)

        # Promote now succeeds -> HYPOTHESIS
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.HYPOTHESIS)

        # 3. Replication needed to proceed to EXPERIMENT
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.HYPOTHESIS) # Needs replications >= 1

        # Replicate successfully
        art = replicate_artifact(art, success=True)
        self.assertEqual(art.replications, 1)

        # Promote succeeds -> EXPERIMENT
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.EXPERIMENT)

        # 4. To get to EVIDENCE, needs replications >= 2, contradiction ratio < 0.20
        art = replicate_artifact(art, success=True) # replications = 2
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.EVIDENCE)

        # 5. To get to THEORY, needs replications >= 3, contradiction ratio < 0.10
        art = replicate_artifact(art, success=True) # replications = 3
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.THEORY)

        # 6. To get to TECHNOLOGY, needs replications >= 10, contradiction ratio < 0.05
        for _ in range(7):
            art = replicate_artifact(art, success=True) # replications = 10
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.TECHNOLOGY)

    def test_artifact_lineage(self):
        parent = KnowledgeArtifact(
            artifact_id="art-parent", title="Relativity", stage=ArtifactStage.THEORY,
            confidence=0.9, replications=5, contradictions=0, novelty=0.8,
            author=AgentId("einstein"), parent_artifact_id=None,
            contributors=(AgentId("einstein"),), created_tick=10
        )
        child = KnowledgeArtifact(
            artifact_id="art-child", title="GPS Tech", stage=ArtifactStage.IDEA,
            confidence=0.5, replications=0, contradictions=0, novelty=0.95,
            author=AgentId("engineer"), parent_artifact_id=parent.artifact_id,
            contributors=(AgentId("einstein"), AgentId("engineer")), created_tick=20
        )

        self.assertEqual(child.parent_artifact_id, "art-parent")
        self.assertIn(AgentId("einstein"), child.contributors)
        self.assertEqual(child.created_tick, 20)

    def test_invalid_transition_rejected(self):
        # Starts with an Idea
        art = KnowledgeArtifact(
            artifact_id="art-skip", title="Skip Stage", stage=ArtifactStage.IDEA,
            confidence=1.0, replications=0, contradictions=0, novelty=0.5,
            author=AgentId("agent-x"), parent_artifact_id=None,
            contributors=(), created_tick=1
        )
        # First promotion can only go to HYPOTHESIS
        art = promote_artifact(art)
        self.assertEqual(art.stage, ArtifactStage.HYPOTHESIS)
        # Stays HYPOTHESIS because it has replications = 0 (violating HYPOTHESIS -> EXPERIMENT rule)
        art_stage_after = promote_artifact(art).stage
        self.assertEqual(art_stage_after, ArtifactStage.HYPOTHESIS)


    def test_review_reputation_weight(self):
        reviewer = ReputationPeerReviewer()
        art = KnowledgeArtifact(
            artifact_id="art-rev", title="Superconductivity", stage=ArtifactStage.HYPOTHESIS,
            confidence=0.5, replications=0, contradictions=0, novelty=0.7,
            author=AgentId("physicist"), parent_artifact_id=None,
            contributors=(), created_tick=5
        )

        # Expert reviewer (reputation = 0.9)
        res_expert = reviewer.evaluate_artifact("expert", 0.9, art, seed=42)
        # Novice reviewer (reputation = 0.1)
        res_novice = reviewer.evaluate_artifact("novice", 0.1, art, seed=42)

        # Reputation weight alters confidence delta magnitude
        self.assertGreater(abs(res_expert.confidence_delta), abs(res_novice.confidence_delta))

    def test_deterministic_replay(self):
        reviewer = ReputationPeerReviewer()
        art = KnowledgeArtifact(
            artifact_id="art-replay", title="Quantum Gravity", stage=ArtifactStage.HYPOTHESIS,
            confidence=0.4, replications=1, contradictions=0, novelty=0.85,
            author=AgentId("string-theorist"), parent_artifact_id=None,
            contributors=(), created_tick=8
        )

        # Multi-evaluation runs with same seed must be completely identical
        res1 = reviewer.evaluate_artifact("rev-1", 0.8, art, seed=100)
        res2 = reviewer.evaluate_artifact("rev-1", 0.8, art, seed=100)

        self.assertEqual(res1.confidence_delta, res2.confidence_delta)
        self.assertEqual(res1.contradiction_found, res2.contradiction_found)

    def test_knowledge_value_function(self):
        val_func = KnowledgeValueFunction()
        art_idea = KnowledgeArtifact(
            artifact_id="art-val", title="Cold Fusion", stage=ArtifactStage.IDEA,
            confidence=0.6, replications=0, contradictions=0, novelty=0.9,
            author=AgentId("chem-a"), parent_artifact_id=None,
            contributors=(), created_tick=2
        )
        art_tech = KnowledgeArtifact(
            artifact_id="art-val", title="Cold Fusion", stage=ArtifactStage.TECHNOLOGY,
            confidence=0.6, replications=10, contradictions=0, novelty=0.9,
            author=AgentId("chem-a"), parent_artifact_id=None,
            contributors=(), created_tick=2
        )

        # Tech value is higher because applicability is 1.0 vs 0.05
        v_idea = val_func.evaluate_value(art_idea)
        v_tech = val_func.evaluate_value(art_tech)

        self.assertGreater(v_tech, v_idea)

    def test_organization_snapshot_and_manager(self):
        from runtime.society.organization import OrganizationStage
        from runtime.society.institution_manager import InstitutionManager
        from runtime.society.organization_events import (
            OrganizationCreatedEvent, MemberJoinedEvent, MemberLeftEvent,
            OrganizationSpecializedEvent, BudgetAllocatedEvent
        )

        manager = InstitutionManager()

        # 1. Create
        create_evt = OrganizationCreatedEvent("org-1", "Alpha Lab", "physics research", AgentId("agent-a"), 1, 0.0)
        manager.apply_event(create_evt)
        
        snap = manager.get_snapshot("org-1")
        self.assertEqual(snap.name, "Alpha Lab")
        self.assertEqual(snap.stage, OrganizationStage.FORMING)
        self.assertEqual(snap.members, (AgentId("agent-a"),))

        # Immutability check
        with self.assertRaises(Exception):
            snap.name = "Beta Lab"

        # 2. Join
        join_evt = MemberJoinedEvent("org-1", AgentId("agent-b"), 1.0)
        manager.apply_event(join_evt)

        snap = manager.get_snapshot("org-1")
        self.assertEqual(len(snap.members), 2)
        # Stage promoted to ACTIVE because members >= 2
        self.assertEqual(snap.stage, OrganizationStage.ACTIVE)

        # 3. Specialize
        spec_evt = OrganizationSpecializedEvent("org-1", ("physics", "nanotech"), 2.0)
        manager.apply_event(spec_evt)

        snap = manager.get_snapshot("org-1")
        self.assertEqual(snap.specialization, ("physics", "nanotech"))
        self.assertEqual(snap.stage, OrganizationStage.SPECIALIZED)

        # 4. Budget replenish
        budget_evt = BudgetAllocatedEvent("org-1", "energy", 500.0, 3.0)
        manager.apply_event(budget_evt)

        self.assertEqual(snap.resources.balances["energy"], 700.0)

        # 5. Leave
        leave_evt = MemberLeftEvent("org-1", AgentId("agent-b"), 4.0)
        manager.apply_event(leave_evt)
        leave_evt_2 = MemberLeftEvent("org-1", AgentId("agent-a"), 5.0)
        manager.apply_event(leave_evt_2)

        snap = manager.get_snapshot("org-1")
        # Stage collapsed because members = 0
        self.assertEqual(snap.stage, OrganizationStage.COLLAPSED)

    def test_organization_utility(self):
        from runtime.society.organization import OrganizationSnapshot, OrganizationStage
        from runtime.society.organization_utility import OrganizationUtilityFunction
        from runtime.economy.resource_budget import ResourceBudget

        utility_func = OrganizationUtilityFunction(coordination_weight=0.1, autonomy_loss=0.2)
        
        # Org with low members (2)
        org_small = OrganizationSnapshot(
            org_id="org-1", name="Alpha", mission="res", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(AgentId("agent-a"), AgentId("agent-b")), reputation=1.0,
            resources=ResourceBudget({"energy": 1000, "attention": 100}), collective_memory=(),
            created_tick=1, research_capacity=50.0, memory_integrity=1.0
        )

        # Org with high members (20) -> higher coordination cost
        org_large = OrganizationSnapshot(
            org_id="org-2", name="Beta", mission="res", specialization=(), stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(20)), reputation=1.0,
            resources=ResourceBudget({"energy": 1000, "attention": 100}), collective_memory=(),
            created_tick=1, research_capacity=50.0, memory_integrity=1.0
        )

        solo_utility = 5.0
        score_small = utility_func.evaluate_join_score("agent-x", org_small, solo_utility)
        score_large = utility_func.evaluate_join_score("agent-x", org_large, solo_utility)

        # Large org coordination cost and split resource share makes small org join score higher!
        self.assertGreater(score_small, score_large)


if __name__ == "__main__":
    unittest.main()
