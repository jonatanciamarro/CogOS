from runtime.society.organization import OrganizationSnapshot, OrganizationStage
from runtime.society.organization_events import (
    OrganizationCreatedEvent, MemberJoinedEvent, MemberLeftEvent
)


class InstitutionDynamics:
    """
    Orchestrates dynamic split (cisão) and mergers (fusão) of organizations
    based on coordination scale-frictions.
    All transitions are performed pure via event emission on the manager.
    """
    def check_splits_and_mergers(self, manager, tick: int, bus=None, ecology_model=None) -> None:
        """
        Scans all active organizations. If size exceeds 15 members,
        splits the group into original lab and a new spinoff lab.
        Enforces formation cost (150 energy, 15 attention) and split cooldowns.
        """
        for org in list(manager.get_all_snapshots()):
            if org.stage in (OrganizationStage.COLLAPSED, OrganizationStage.FORMING):
                continue

            # Split logic if members exceed size limit (15) and org age is at least 30 ticks
            if len(org.members) > 15:
                # Add split cooldown of 30 ticks to allow institutions to stabilize and research
                if tick - org.created_tick < 30:
                    continue

                # 1. Budget check: Parent org must have enough resources for split fee
                energy_cost = 150
                attention_cost = 15
                if (org.resources.balances.get("energy", 0) < energy_cost or 
                    org.resources.balances.get("attention", 0) < attention_cost):
                    # Not enough resources to pay the administrative split fee; split fails
                    continue

                # Deduct from parent organization
                org.resources.consume("energy", energy_cost)
                org.resources.consume("attention", attention_cost)

                members = list(org.members)
                half = len(members) // 2

                group1 = members[:half]
                group2 = members[half:]

                # Apply cooldowns to leaving members
                if ecology_model is not None:
                    for m in group2:
                        ecology_model.apply_cooldown(m, tick)

                # 2. Second half leaves original organization
                for m in group2:
                    left_evt = MemberLeftEvent(
                        org_id=org.org_id,
                        member_id=m,
                        timestamp=float(tick)
                    )
                    manager.apply_event(left_evt)
                    if bus:
                        bus.publish("MemberLeftEvent", left_evt)

                # 3. Calculate inherited reputation
                founder_rep = org.reputation
                inherited_rep = 1.0
                if ecology_model is not None:
                    inherited_rep = ecology_model.calculate_inherited_reputation(founder_rep)

                # Spinoff DNA inheritance
                from runtime.society.organization import InstitutionDNA
                import random
                import dataclasses

                seed_val = tick + hash(org.org_id)
                rnd = random.Random(seed_val)

                parent_dna = org.dna
                if parent_dna is None:
                    parent_dna = InstitutionDNA(
                        procedural_traits=("empirical",),
                        cognitive_traits=(0.5, 0.5, 0.5),
                        cultural_traits=("collaboration",),
                        preferred_niches=("physics", "biology", "general")
                    )

                # Calculate dynamic mutation rate under pressure
                mutation_rate = parent_dna.mutation_rate
                if ecology_model is not None:
                    env_stress = 0.9 if tick >= 50 else 0.1
                    last_active = org.last_active_research_tick if org.last_active_research_tick is not None else org.created_tick
                    stagnation = min(1.0, max(0.0, (tick - last_active) / 100.0))
                    res_pressure = min(1.0, max(0.0, 1.0 - (org.resources.balances.get("energy", 0) / 1000.0)))
                    mutation_rate = ecology_model.calculate_mutation_pressure(env_stress, stagnation, res_pressure)

                mutated_cognitive = tuple(
                    max(0.0, min(1.0, val + rnd.uniform(-mutation_rate, mutation_rate)))
                    for val in parent_dna.cognitive_traits
                )

                procedural = list(parent_dna.procedural_traits)
                if rnd.random() < mutation_rate:
                    procedural.append(f"method-{tick}")

                cultural = list(parent_dna.cultural_traits)
                if rnd.random() < mutation_rate:
                    cultural.append(f"principle-{tick}")

                # Inherit niches with potential mutation
                niches = list(parent_dna.preferred_niches) if parent_dna.preferred_niches else ["general"]
                if rnd.random() < mutation_rate:
                    possible_niches = ["ai", "neuroscience", "complex_systems", "materials", "chemistry", "medicine"]
                    new_niche = rnd.choice(possible_niches)
                    if new_niche not in niches:
                        niches.append(new_niche)
                if len(niches) > 2 and rnd.random() < mutation_rate:
                    niches.pop(rnd.randint(0, len(niches) - 1))

                spinoff_dna = InstitutionDNA(
                    procedural_traits=tuple(procedural),
                    cognitive_traits=tuple(mutated_cognitive),
                    cultural_traits=tuple(cultural),
                    preferred_niches=tuple(niches),
                    mutation_rate=mutation_rate,
                    lineage_depth=parent_dna.lineage_depth + 1,
                    parent_org_id=org.org_id
                )


                # 4. Second half forms a new spin-off organization
                new_org_id = f"{org.org_id}-spinoff"
                create_evt = OrganizationCreatedEvent(
                    org_id=new_org_id,
                    name=f"{org.name} Spinoff",
                    mission=f"advanced {org.mission}",
                    creator=group2[0],
                    created_tick=tick,
                    timestamp=float(tick)
                )
                manager.apply_event(create_evt)

                # Spinoff inherits parent collective memory (70% probability per item)
                inherited_mem = tuple(
                    art for art in org.collective_memory
                    if rnd.random() <= 0.70
                )

                # Update spinoff reputation, dna, collective memory, and research timeline in manager snapshot
                spinoff_snap = manager.get_snapshot(new_org_id)
                if spinoff_snap:
                    spinoff_snap = dataclasses.replace(
                        spinoff_snap,
                        reputation=inherited_rep,
                        dna=spinoff_dna,
                        collective_memory=inherited_mem,
                        last_active_research_tick=tick
                    )
                    manager._snapshots[new_org_id] = spinoff_snap




                if bus:
                    bus.publish("OrganizationCreatedEvent", create_evt)

                # 5. Rest of second half joins the spinoff
                for m in group2[1:]:
                    join_evt = MemberJoinedEvent(
                        org_id=new_org_id,
                        member_id=m,
                        timestamp=float(tick)
                    )
                    manager.apply_event(join_evt)
                    if bus:
                        bus.publish("MemberJoinedEvent", join_evt)
