import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage, InstitutionDNA
from runtime.society.organization_events import OrganizationCreatedEvent, MemberJoinedEvent
from runtime.society.institution_manager import InstitutionManager
from runtime.society.institution_dynamics import InstitutionDynamics
from runtime.society.institution_ecology import InstitutionEcologyModel
from runtime.economy.resource_budget import ResourceBudget


class TestNaturalSelection(unittest.TestCase):

    def test_dna_drift(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        # Create parent org
        create_evt = OrganizationCreatedEvent("org-parent", "Parent Lab", "physics", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        import dataclasses
        snap = manager.get_snapshot("org-parent")
        snap.resources.replenish("energy", 500)
        snap.resources.replenish("attention", 50)

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

        # Trigger spinoff split at tick 40
        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)

        spinoff1 = manager.get_snapshot("org-parent-spinoff")
        self.assertIsNotNone(spinoff1)
        self.assertEqual(spinoff1.dna.lineage_depth, 2)
        
        # Verify DNA mutated slightly (drifted)
        self.assertNotEqual(spinoff1.dna.cognitive_traits, (0.5, 0.5, 0.5))

    def test_selection_pressure(self):
        ecology = InstitutionEcologyModel()

        # Create two orgs: orgA (active research, high reputation) vs orgB (empty, no discoveries)
        from runtime.science.artifact import KnowledgeArtifact
        from runtime.science.artifact_stage import ArtifactStage
        
        tech_art = KnowledgeArtifact("art-1", "Tech", ArtifactStage.TECHNOLOGY, 0.9, 1, 0, 0.5, AgentId("creator"), None, (), 1, 1.0)
        
        orgA = OrganizationSnapshot(
            org_id="org-A", name="A", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"member-a-{i}") for i in range(8)), reputation=4.5,
            resources=ResourceBudget({"energy": 500, "attention": 50}), collective_memory=(tech_art,),
            created_tick=1, research_capacity=20.0, memory_integrity=1.0,
            dna=InstitutionDNA(
                procedural_traits=("empirical",),
                cognitive_traits=(0.8, 0.7, 0.9),  # high exploration
                cultural_traits=("collaboration",)
            )
        )

        orgB = OrganizationSnapshot(
            org_id="org-B", name="B", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(), reputation=1.0,
            resources=ResourceBudget({"energy": 50, "attention": 5}), collective_memory=(),
            created_tick=1, research_capacity=5.0, memory_integrity=0.3,
            dna=InstitutionDNA(
                procedural_traits=("empirical",),
                cognitive_traits=(0.2, 0.1, 0.1),
                cultural_traits=("collaboration",)
            )
        )

        fitnessA = ecology.calculate_fitness(orgA, tick=10)
        fitnessB = ecology.calculate_fitness(orgB, tick=10)

        # High-performing institution should have significantly higher fitness than stagnated/empty org
        self.assertGreater(fitnessA, fitnessB)


if __name__ == "__main__":
    unittest.main()
