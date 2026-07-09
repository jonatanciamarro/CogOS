from runtime.society.organization import OrganizationSnapshot, OrganizationStage
from runtime.society.organization_events import (
    OrganizationCreatedEvent, MemberJoinedEvent, MemberLeftEvent,
    OrganizationSpecializedEvent, BudgetAllocatedEvent, OrganizationCollapsedEvent
)
from runtime.economy.resource_budget import ResourceBudget


class InstitutionManager:
    """
    InstitutionManager tracks and mutates OrganizationSnapshots by replaying
    institutional transaction events.
    Never modifies state in-place.
    """
    def __init__(self):
        self._snapshots: dict[str, OrganizationSnapshot] = {}
        self._history: list = []

    def get_snapshot(self, org_id: str) -> OrganizationSnapshot | None:
        """Retrieves the latest snapshot of an organization."""
        return self._snapshots.get(org_id)

    def get_all_snapshots(self) -> list[OrganizationSnapshot]:
        return list(self._snapshots.values())

    def apply_event(self, event) -> None:
        """
        Applies a transaction event and transitions the organization snapshot.
        """
        self._history.append(event)

        if isinstance(event, OrganizationCreatedEvent):
            # Form forming organization snapshot
            from runtime.society.organization import InstitutionDNA
            snap = OrganizationSnapshot(
                org_id=event.org_id,
                name=event.name,
                mission=event.mission,
                specialization=(),
                stage=OrganizationStage.FORMING,
                members=(event.creator,),
                reputation=1.0,
                resources=ResourceBudget({"energy": 200, "attention": 20}),
                collective_memory=(),
                created_tick=event.created_tick,
                research_capacity=10.0,
                memory_integrity=1.0,
                dna=InstitutionDNA(
                    procedural_traits=("empirical",),
                    cognitive_traits=(0.5, 0.5, 0.5),  # (abstraction, risk_tolerance, exploration)
                    cultural_traits=("collaboration",),
                    preferred_niches=("physics", "biology", "general")
                ),

                dormant_since_tick=None,
                revival_until_tick=None,
                last_active_research_tick=event.created_tick
            )
            self._snapshots[event.org_id] = snap

        elif isinstance(event, MemberJoinedEvent):
            prev = self._snapshots.get(event.org_id)
            if prev and event.member_id not in prev.members:
                new_members = prev.members + (event.member_id,)
                # Elevate to ACTIVE if we have multiple members
                new_stage = prev.stage
                if prev.stage == OrganizationStage.FORMING and len(new_members) >= 2:
                    new_stage = OrganizationStage.ACTIVE

                # Logistic reputation curve: Delta R = gain * (1 - R/5.0)
                gain = 0.10
                delta_r = gain * (1.0 - (prev.reputation / 5.0))
                new_rep = min(5.0, prev.reputation + delta_r)

                self._snapshots[event.org_id] = OrganizationSnapshot(
                    org_id=prev.org_id,
                    name=prev.name,
                    mission=prev.mission,
                    specialization=prev.specialization,
                    stage=new_stage,
                    members=new_members,
                    reputation=new_rep,
                    resources=prev.resources,
                    collective_memory=prev.collective_memory,
                    created_tick=prev.created_tick,
                    research_capacity=prev.research_capacity + 5.0,
                    memory_integrity=prev.memory_integrity,
                    dna=prev.dna,
                    dormant_since_tick=prev.dormant_since_tick,
                    revival_until_tick=prev.revival_until_tick,
                    last_active_research_tick=prev.last_active_research_tick
                )

        elif isinstance(event, MemberLeftEvent):
            prev = self._snapshots.get(event.org_id)
            if prev and event.member_id in prev.members:
                new_members = tuple(m for m in prev.members if m != event.member_id)
                new_stage = prev.stage
                if len(new_members) == 0:
                    new_stage = OrganizationStage.COLLAPSED

                self._snapshots[event.org_id] = OrganizationSnapshot(
                    org_id=prev.org_id,
                    name=prev.name,
                    mission=prev.mission,
                    specialization=prev.specialization,
                    stage=new_stage,
                    members=new_members,
                    reputation=max(0.0, prev.reputation - 0.2),
                    resources=prev.resources,
                    collective_memory=prev.collective_memory,
                    created_tick=prev.created_tick,
                    research_capacity=max(0.0, prev.research_capacity - 5.0),
                    memory_integrity=prev.memory_integrity,
                    dna=prev.dna,
                    dormant_since_tick=prev.dormant_since_tick,
                    revival_until_tick=prev.revival_until_tick,
                    last_active_research_tick=prev.last_active_research_tick
                )

        elif isinstance(event, OrganizationSpecializedEvent):
            prev = self._snapshots.get(event.org_id)
            if prev:
                # Logistic reputation curve for specialization
                gain = 0.30
                delta_r = gain * (1.0 - (prev.reputation / 5.0))
                new_rep = min(5.0, prev.reputation + delta_r)

                self._snapshots[event.org_id] = OrganizationSnapshot(
                    org_id=prev.org_id,
                    name=prev.name,
                    mission=prev.mission,
                    specialization=event.specializations,
                    stage=OrganizationStage.SPECIALIZED,
                    members=prev.members,
                    reputation=new_rep,
                    resources=prev.resources,
                    collective_memory=prev.collective_memory,
                    created_tick=prev.created_tick,
                    research_capacity=prev.research_capacity + 10.0,
                    memory_integrity=prev.memory_integrity,
                    dna=prev.dna,
                    dormant_since_tick=prev.dormant_since_tick,
                    revival_until_tick=prev.revival_until_tick,
                    last_active_research_tick=prev.last_active_research_tick
                )

        elif isinstance(event, BudgetAllocatedEvent):
            prev = self._snapshots.get(event.org_id)
            if prev:
                prev.resources.replenish(event.resource_type.lower(), int(event.amount))

        elif isinstance(event, OrganizationCollapsedEvent):
            prev = self._snapshots.get(event.org_id)
            if prev:
                self._snapshots[event.org_id] = OrganizationSnapshot(
                    org_id=prev.org_id,
                    name=prev.name,
                    mission=prev.mission,
                    specialization=prev.specialization,
                    stage=OrganizationStage.COLLAPSED,
                    members=(),
                    reputation=0.0,
                    resources=prev.resources,
                    collective_memory=prev.collective_memory,
                    created_tick=prev.created_tick,
                    research_capacity=0.0,
                    memory_integrity=0.0,
                    dna=prev.dna,
                    dormant_since_tick=prev.dormant_since_tick,
                    revival_until_tick=prev.revival_until_tick,
                    last_active_research_tick=prev.last_active_research_tick
                )
