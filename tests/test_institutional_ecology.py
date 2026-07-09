import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage
from runtime.society.organization_events import OrganizationCreatedEvent, MemberJoinedEvent
from runtime.society.institution_manager import InstitutionManager
from runtime.society.institution_dynamics import InstitutionDynamics
from runtime.society.institution_ecology import InstitutionEcologyModel
from runtime.economy.resource_budget import ResourceBudget


class TestInstitutionalEcology(unittest.TestCase):

    def test_org_creation_fails_without_budget(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        # Create parent org with poor resources (e.g. 50 energy, less than 150)
        create_evt = OrganizationCreatedEvent("org-poor", "Poor Lab", "science", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        # Set low resources
        snap = manager.get_snapshot("org-poor")
        snap.resources.balances["energy"] = 50
        snap.resources.balances["attention"] = 20

        # Add 16 members to trigger split
        import dataclasses
        snap = dataclasses.replace(
            snap,
            stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(16))
        )
        manager._snapshots["org-poor"] = snap

        # Split should fail due to lack of budget
        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)

        spinoff = manager.get_snapshot("org-poor-spinoff")
        self.assertIsNone(spinoff)  # No spinoff created

    def test_spinoff_inherits_founder_reputation(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        # Creator has a specific reputation, parent org reputation is e.g. 3.0
        create_evt = OrganizationCreatedEvent("org-parent", "Parent Lab", "science", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        import dataclasses
        snap = manager.get_snapshot("org-parent")
        snap.resources.replenish("energy", 300)
        snap.resources.replenish("attention", 30) # fill budget

        snap = dataclasses.replace(
            snap,
            stage=OrganizationStage.ACTIVE,
            reputation=3.0,
            members=tuple(AgentId(f"agent-{i}") for i in range(16))
        )
        manager._snapshots["org-parent"] = snap

        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)

        spinoff = manager.get_snapshot("org-parent-spinoff")
        self.assertIsNotNone(spinoff)

        # Expected inherited reputation: (0.3 * 3.0 + 0.7 * 1.0) = 1.6 + logistic member join increments = 2.0483
        self.assertAlmostEqual(spinoff.reputation, 2.0483, places=3)



    def test_large_lab_splits_once_not_infinitely(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()
        ecology = InstitutionEcologyModel()

        create_evt = OrganizationCreatedEvent("org-rich", "Rich Lab", "science", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        import dataclasses
        snap = manager.get_snapshot("org-rich")
        snap.resources.replenish("energy", 1000)
        snap.resources.replenish("attention", 100)

        # Add 18 members
        snap = dataclasses.replace(
            snap,
            stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(18))
        )
        manager._snapshots["org-rich"] = snap

        # First split
        dynamics.check_splits_and_mergers(manager, tick=40, ecology_model=ecology)
        
        # Second split check immediately at tick 41
        # Leaving members are on cooldown, spinoff size is 9 (< 15), parent size is 9 (< 15)
        # No further splits should occur
        dynamics.check_splits_and_mergers(manager, tick=41, ecology_model=ecology)


        spinoff2 = manager.get_snapshot("org-rich-spinoff-spinoff")
        self.assertIsNone(spinoff2)

    def test_active_research_preserves_memory(self):
        ecology = InstitutionEcologyModel()

        # No citations/replications: decay = 0.01
        decay_none = ecology.calculate_memory_decay(citations=0, replications=0)
        self.assertAlmostEqual(decay_none, 0.01)

        # High citations and replications: decay decreases (knowledge preserved)
        decay_high = ecology.calculate_memory_decay(citations=10, replications=20)
        self.assertLess(decay_high, decay_none)
        self.assertGreaterEqual(decay_high, 0.001)


if __name__ == "__main__":
    unittest.main()
