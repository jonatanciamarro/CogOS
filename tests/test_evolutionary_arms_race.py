import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage, InstitutionDNA, SPECIES_MODIFIERS
from runtime.society.organization_events import OrganizationCreatedEvent, MemberJoinedEvent
from runtime.society.institution_manager import InstitutionManager
from runtime.society.institution_dynamics import InstitutionDynamics
from runtime.society.institution_ecology import InstitutionEcologyModel
from runtime.civilization.world import World
from runtime.civilization.environment import Environment
from runtime.observability.ecology_metrics import InstitutionDiversityIndex, InstitutionalRecoveryIndex
from runtime.observability.metric import MetricContext


class TestEvolutionaryArmsRace(unittest.TestCase):

    def test_niche_monoculture(self):
        # Create metric context with active organizations all having standard/same species profile
        org1 = OrganizationSnapshot(
            org_id="org-1", name="A", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(), reputation=2.0, resources=None, collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0,
            dna=InstitutionDNA(
                procedural_traits=("empirical",),
                cognitive_traits=(0.5, 0.5, 0.5), # maps to STANDARD_RESEARCH_UNIT
                cultural_traits=(),
                preferred_niches=("physics",)
            )
        )

        org2 = OrganizationSnapshot(
            org_id="org-2", name="B", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=(), reputation=2.0, resources=None, collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0,
            dna=InstitutionDNA(
                procedural_traits=("empirical",),
                cognitive_traits=(0.5, 0.5, 0.5), # maps to STANDARD_RESEARCH_UNIT
                cultural_traits=(),
                preferred_niches=("physics",)
            )
        )

        class MockSettlement:
            institutions = [org1, org2]

        class MockCivilization:
            settlements = [MockSettlement()]

        class MockWorld:
            civilizations = [MockCivilization()]

        # Compute Shannon IDI (entropy)
        ctx = MetricContext(tick=10, events=[], world_snapshot=MockWorld())
        idi_calc = InstitutionDiversityIndex()
        idi = idi_calc.compute(ctx)
        
        # Diversity must be 0.0 because all belong to the same species profile
        self.assertEqual(idi, 0.0)

    def test_ecological_collapse(self):
        world = World()
        # Initial stress is 0.1
        self.assertEqual(world.evolution_pressure.environmental_stress, 0.1)

        # Trigger decay
        world.tick(None)
        # Stays at lower boundary 0.1
        self.assertEqual(world.evolution_pressure.environmental_stress, 0.1)

    def test_speciation_drift(self):
        # Test modifiers mapping
        mod_explorer = SPECIES_MODIFIERS["INNOVATIVE_EXPLORER"]
        self.assertGreater(mod_explorer.discovery_speed, 1.0)
        self.assertLess(mod_explorer.memory_retention, 1.0)


if __name__ == "__main__":
    unittest.main()
