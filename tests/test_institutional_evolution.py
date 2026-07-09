import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage, InstitutionDNA
from runtime.society.organization_events import OrganizationCreatedEvent, MemberJoinedEvent, OrganizationCollapsedEvent
from runtime.society.institution_manager import InstitutionManager
from runtime.society.institution_dynamics import InstitutionDynamics
from runtime.society.institution_ecology import InstitutionEcologyModel
from runtime.economy.resource_budget import ResourceBudget


class TestInstitutionalEvolution(unittest.TestCase):

    def test_spinoff_preserves_parent_lineage(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        # Create parent lab
        create_evt = OrganizationCreatedEvent("org-parent", "Parent Lab", "physics", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        # Set resources and members
        import dataclasses
        snap = manager.get_snapshot("org-parent")
        snap.resources.replenish("energy", 300)
        snap.resources.replenish("attention", 30)

        # Set parent DNA
        parent_dna = InstitutionDNA(
            procedural_traits=("empirical",),
            cognitive_traits=(0.5, 0.5, 0.5),
            cultural_traits=("collaboration",),
            lineage_depth=1,
            parent_org_id=None
        )

        snap = dataclasses.replace(
            snap,
            stage=OrganizationStage.ACTIVE,
            dna=parent_dna,
            members=tuple(AgentId(f"agent-{i}") for i in range(16))
        )
        manager._snapshots["org-parent"] = snap

        # Trigger spinoff split
        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)

        spinoff = manager.get_snapshot("org-parent-spinoff")
        self.assertIsNotNone(spinoff)
        self.assertEqual(spinoff.dna.lineage_depth, 2)
        self.assertEqual(spinoff.dna.parent_org_id, "org-parent")

    def test_mutation_bounded(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        create_evt = OrganizationCreatedEvent("org-parent", "Parent Lab", "physics", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        import dataclasses
        snap = manager.get_snapshot("org-parent")
        snap.resources.replenish("energy", 300)
        snap.resources.replenish("attention", 30)

        # Set parent DNA close to boundaries
        parent_dna = InstitutionDNA(
            procedural_traits=("empirical",),
            cognitive_traits=(0.98, 0.02, 0.5),
            cultural_traits=("collaboration",),
            lineage_depth=1,
            parent_org_id=None
        )

        snap = dataclasses.replace(
            snap,
            stage=OrganizationStage.ACTIVE,
            dna=parent_dna,
            members=tuple(AgentId(f"agent-{i}") for i in range(16))
        )
        manager._snapshots["org-parent"] = snap

        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)

        spinoff = manager.get_snapshot("org-parent-spinoff")
        self.assertIsNotNone(spinoff)
        # Mutations must be clamped between 0.0 and 1.0
        for val in spinoff.dna.cognitive_traits:
            self.assertTrue(0.0 <= val <= 1.0)

    def test_declining_org_can_recover(self):
        ecology = InstitutionEcologyModel()
        
        # Budget failure (energy=0), low members, low memory integrity -> score > 0.60 (DECLINING)
        org = OrganizationSnapshot(
            org_id="org-test", name="T", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(AgentId("agent-1"),), reputation=4.0,
            resources=ResourceBudget({"energy": 5, "attention": 10}), collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=0.1
        )

        score = ecology.evaluate_collapse_score(org)
        self.assertGreater(score, 0.60)
        self.assertLessEqual(score, 1.0) # score should trigger decline but not collapse

    def test_extinction_cleanup(self):
        manager = InstitutionManager()
        
        # Apply collapse event (passing 3 arguments: org_id, reason, timestamp)
        collapse_evt = OrganizationCollapsedEvent("org-test", "bankruptcy", 1.0)
        # Mock active snapshot in manager
        org = OrganizationSnapshot(
            org_id="org-test", name="T", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(AgentId("agent-1"),), reputation=4.0,
            resources=ResourceBudget({"energy": 200, "attention": 20}), collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0
        )
        manager._snapshots["org-test"] = org

        manager.apply_event(collapse_evt)

        collapsed = manager.get_snapshot("org-test")
        self.assertEqual(collapsed.stage, OrganizationStage.COLLAPSED)
        self.assertEqual(len(collapsed.members), 0)
        self.assertEqual(collapsed.reputation, 0.0)


if __name__ == "__main__":
    unittest.main()
