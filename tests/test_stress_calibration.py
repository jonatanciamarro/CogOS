import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.types import AgentId
from runtime.society.organization import OrganizationSnapshot, OrganizationStage
from runtime.society.organization_utility import OrganizationUtilityFunction
from runtime.society.institution_dynamics import InstitutionDynamics
from runtime.society.institution_manager import InstitutionManager
from runtime.economy.resource_budget import ResourceBudget


class TestStressCalibration(unittest.TestCase):

    def test_hybrid_coordination_cost_and_autonomy_loss(self):
        # High coordination cost weight
        utility_func = OrganizationUtilityFunction(coordination_weight=0.2, autonomy_loss=0.3)

        # 1. Group of 5 members
        org_small = OrganizationSnapshot(
            org_id="small", name="S", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(5)), reputation=1.0,
            resources=ResourceBudget({"energy": 100, "attention": 10}), collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0
        )

        # 2. Group of 30 members (bureaucracy explosion)
        org_large = OrganizationSnapshot(
            org_id="large", name="L", mission="M", specialization=(), stage=OrganizationStage.ACTIVE,
            members=tuple(AgentId(f"agent-{i}") for i in range(30)), reputation=1.0,
            resources=ResourceBudget({"energy": 100, "attention": 10}), collective_memory=(),
            created_tick=1, research_capacity=10.0, memory_integrity=1.0
        )

        solo_util = 4.0
        score_small = utility_func.evaluate_join_score("agent-x", org_small, solo_util)
        score_large = utility_func.evaluate_join_score("agent-x", org_large, solo_util)

        # Large group coordination cost grows by N^1.5 + log(N), heavily penalizing scale
        self.assertGreater(score_small, score_large)
        self.assertLess(score_large, 0.0)

    def test_institution_dynamics_splits_overloaded_lab(self):
        manager = InstitutionManager()
        dynamics = InstitutionDynamics()

        # Create laboratory and join 16 members (limit is 15)
        from runtime.society.organization_events import OrganizationCreatedEvent, MemberJoinedEvent
        create_evt = OrganizationCreatedEvent("org-big", "Mega Lab", "physics", AgentId("creator"), 1, 0.0)
        manager.apply_event(create_evt)

        for i in range(16):
            join_evt = MemberJoinedEvent("org-big", AgentId(f"member-{i}"), 1.0)
            manager.apply_event(join_evt)

        # Apply dynamics check at tick 40 (satisfying minimum age requirement)
        dynamics.check_splits_and_mergers(manager, tick=40)


        # Reconstructed snapshots
        original = manager.get_snapshot("org-big")
        spinoff = manager.get_snapshot("org-big-spinoff")

        self.assertIsNotNone(original)
        self.assertIsNotNone(spinoff)

        # Members are split into two laboratories
        self.assertLess(len(original.members), 16)
        self.assertGreater(len(spinoff.members), 0)


if __name__ == "__main__":
    unittest.main()
