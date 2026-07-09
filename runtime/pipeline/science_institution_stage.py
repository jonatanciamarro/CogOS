import uuid
from runtime.society.organization import OrganizationSnapshot, OrganizationStage, SPECIES_MODIFIERS

from runtime.society.organization_events import (
    OrganizationCreatedEvent, MemberJoinedEvent, MemberLeftEvent,
    BudgetAllocatedEvent, ResearchStartedEvent, ResearchCompletedEvent,
    OrganizationCollapsedEvent, SpeciationEvent, AdaptationEvent, ExtinctionEvent
)
from runtime.evolution.phylogeny import PhylogenyTracker
from runtime.evolution.fossil import FossilRecord, ExtinctSpeciesRecord

from runtime.society.institution_manager import InstitutionManager
from runtime.society.organization_utility import OrganizationUtilityFunction
from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_stage import ArtifactStage
from runtime.science.artifact_lifecycle import promote_artifact, replicate_artifact, review_artifact
from runtime.science.peer_review import ReputationPeerReviewer
from runtime.economy.types import AgentId


class ScienceInstitutionStage:
    """
    Pluggable simulation pipeline stage managing coalition updates,
    shared resource pooling, and collective artifact lifecycle transitions.
    """
    name = "science_institution"

    def _handle_energy_collapse(self, event_type, payload) -> None:
        if hasattr(self, "_current_world") and self._current_world:
            self._current_world.evolution_pressure.environmental_stress = min(
                1.0, self._current_world.evolution_pressure.environmental_stress + 0.40
            )

    def _handle_research_completed(self, event_type, payload) -> None:
        if hasattr(self, "_current_world") and self._current_world:
            self._current_world.evolution_pressure.scientific_pressure = min(
                1.0, self._current_world.evolution_pressure.scientific_pressure + 0.15
            )

    def run(self, ctx, world, state: dict) -> None:
        if not hasattr(self, "_subscribed"):
            self._current_world = world
            ctx.bus.subscribe("EnergyCollapseEvent", self._handle_energy_collapse)
            ctx.bus.subscribe("ResearchCompletedEvent", self._handle_research_completed)
            self._subscribed = True
        else:
            self._current_world = world

        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})

        # Resolve managers and inputs
        manager = ctx.registry.resolve(InstitutionManager)
        agents = state.get("agents_by_id", {})
        tick = state.get("current_tick", 0)

        util_calc = OrganizationUtilityFunction()
        reviewer = ReputationPeerReviewer()

        # Resolve or register phylogeny tracker and fossil records
        try:
            tracker = ctx.registry.resolve(PhylogenyTracker)
        except KeyError:
            tracker = PhylogenyTracker()
            ctx.registry.register(PhylogenyTracker, tracker)

        try:
            fossil_record = ctx.registry.resolve(FossilRecord)
        except KeyError:
            fossil_record = FossilRecord()
            ctx.registry.register(FossilRecord, fossil_record)

        # Resolve or register InstitutionEcologyModel
        from runtime.society.institution_ecology import InstitutionEcologyModel
        try:
            ecology_model = ctx.registry.resolve(InstitutionEcologyModel)
        except KeyError:
            ecology_model = InstitutionEcologyModel()
            ctx.registry.register(InstitutionEcologyModel, ecology_model)

        # Register births of any new snapshot organization
        for org in manager.get_all_snapshots():
            if org.org_id not in tracker.nodes:
                tracker.register_birth(
                    org_id=org.org_id,
                    parent_id=org.dna.parent_org_id if org.dna else None,
                    profile=org.speciation_profile,
                    tick=float(tick)
                )

        # 1. Coalition Formation Loops
        organizations = manager.get_all_snapshots()
        active_orgs = [o for o in organizations if o.stage != OrganizationStage.COLLAPSED]

        # Auto-create Laboratory if none exists to boot sim
        if not active_orgs and len(agents) >= 2:
            agent_list = list(agents.values())
            creator = agent_list[0]
            org_id = "org-alpha"
            create_evt = OrganizationCreatedEvent(
                org_id=org_id,
                name="Alpha Laboratory",
                mission="scientific breakthrough",
                creator=creator.identity.agent_id,
                created_tick=tick,
                timestamp=float(tick)
            )
            manager.apply_event(create_evt)
            active_orgs = [manager.get_snapshot(org_id)]

        for org in active_orgs:
            for agent in list(agents.values()):
                # Default solo utility representation
                solo_utility = 4.0
                join_score = util_calc.evaluate_join_score(agent, org, solo_utility, tick, ecology_model)

                if agent.identity.agent_id in org.members:
                    # Leave coordination evaluation
                    if join_score < -0.5:
                        leave_evt = MemberLeftEvent(org.org_id, agent.identity.agent_id, float(tick))
                        manager.apply_event(leave_evt)
                else:
                    # Join evaluation
                    if join_score > 0.10:
                        join_evt = MemberJoinedEvent(org.org_id, agent.identity.agent_id, float(tick))
                        manager.apply_event(join_evt)

        # Trigger splits and mergers dynamics
        from runtime.society.institution_dynamics import InstitutionDynamics
        dynamics = InstitutionDynamics()
        dynamics.check_splits_and_mergers(manager, tick, ctx.bus, ecology_model)

        # Resource pooling: members pool resources into their organization budget
        for org in manager.get_all_snapshots():
            if org.stage == OrganizationStage.COLLAPSED:
                continue
            for member_id in org.members:
                member_agent = agents.get(member_id)
                if member_agent:
                    # Deduct from member budget and replenish shared pool
                    m_budget = member_agent.resource_budget
                    if m_budget.balances.get("energy", 0) >= 30:
                        m_budget.consume("energy", 30)
                        org.resources.replenish("energy", 30)
                    if m_budget.balances.get("attention", 0) >= 3:
                        m_budget.consume("attention", 3)
                        org.resources.replenish("attention", 3)

            # Friction: resource leakage based on size of group
            leak_energy = int(0.5 * len(org.members))
            leak_att = int(0.1 * len(org.members))
            if org.resources.balances.get("energy", 0) >= leak_energy:
                org.resources.consume("energy", leak_energy)
            if org.resources.balances.get("attention", 0) >= leak_att:
                org.resources.consume("attention", leak_att)

        # 2. Collective Resource Pooling & Experiments
        # Pre-compute niche congestion counts (carrying capacity K=3 per niche)
        active_snaps = [o for o in manager.get_all_snapshots() if o.stage != OrganizationStage.COLLAPSED]
        niche_counts: dict = {}
        for o in active_snaps:
            if o.dna and o.dna.preferred_niches:
                for n in o.dna.preferred_niches:
                    niche_counts[n] = niche_counts.get(n, 0) + 1

        for org in active_snaps:
            if org.stage == OrganizationStage.DORMANT:
                continue

            modifier = SPECIES_MODIFIERS.get(org.speciation_profile)
            if modifier is None:
                from runtime.society.organization import SpeciationModifier
                modifier = SpeciationModifier(1.0, 1.0, 1.0, 1.0)

            # Niche congestion pressure: P = N_in_niche / K
            niche_selected = "general"
            if org.dna and org.dna.preferred_niches:
                import random
                rnd = random.Random(tick + hash(org.org_id))
                niche_selected = rnd.choice(org.dna.preferred_niches)
            niche_pressure = niche_counts.get(niche_selected, 0) / 3.0

            # Modified research costs: SpeciationModifier * niche congestion
            energy_cost = int(50 * modifier.energy_cost * (1.0 + niche_pressure * 0.1))
            attention_cost = int(5 * modifier.energy_cost * (1.0 + niche_pressure * 0.1))

            if org.resources.balances.get("energy", 0) >= energy_cost and org.resources.balances.get("attention", 0) >= attention_cost:
                org.resources.consume("energy", energy_cost)
                org.resources.consume("attention", attention_cost)

                import dataclasses
                org = dataclasses.replace(org, last_active_research_tick=tick)
                manager._snapshots[org.org_id] = org

                from runtime.science.knowledge_repository import KnowledgeRepository
                try:
                    repo = ctx.registry.resolve(KnowledgeRepository)
                except KeyError:
                    repo = KnowledgeRepository()
                    ctx.registry.register(KnowledgeRepository, repo)

                artifacts = repo.get_all_artifacts()
                active_arts = [a for a in artifacts if a.stage != ArtifactStage.TECHNOLOGY]

                if not active_arts:
                    art_id = f"art-{uuid.uuid4().hex[:6]}"
                    art = KnowledgeArtifact(
                        artifact_id=art_id,
                        title=f"Cooperative Discovery {art_id}",
                        stage=ArtifactStage.IDEA,
                        confidence=0.5,
                        replications=0,
                        contradictions=0,
                        novelty=0.8,
                        author=org.members[0] if org.members else AgentId("system"),
                        parent_artifact_id=None,
                        contributors=org.members,
                        created_tick=tick,
                        niche=niche_selected,
                        origin_species=org.speciation_profile
                    )
                    repo.register_artifact(art)
                    ctx.bus.publish("ResearchStartedEvent", ResearchStartedEvent(org.org_id, art_id, float(tick)))
                else:
                    art = active_arts[0]

                    if art.stage == ArtifactStage.IDEA:
                        res = reviewer.evaluate_artifact(
                            org.members[0] if org.members else AgentId("system"),
                            0.8, art, seed=tick
                        )
                        # Apply speciation multipliers; dampen if niche congested
                        confidence_gain = (
                            res.confidence_delta
                            * modifier.innovation_bonus
                            * modifier.discovery_speed
                            / (1.0 + niche_pressure * 0.05)
                        )
                        art = review_artifact(art, confidence_gain)
                        import dataclasses
                        new_rep = ecology_model.calculate_logistic_reputation_gain(org.reputation, 0.05 * res.confidence_delta)
                        updated_org = dataclasses.replace(org, reputation=new_rep)
                        manager._snapshots[org.org_id] = updated_org
                    else:
                        art = replicate_artifact(art, success=True)

                    promoted = promote_artifact(art)

                    # Theorists have a harder time converting to technology
                    if promoted.stage == ArtifactStage.TECHNOLOGY:
                        import random
                        rnd = random.Random(tick + hash(org.org_id))
                        success_rate = 0.30 if org.speciation_profile == "ACADEMIC_THEORIST" else 0.90
                        if rnd.random() > success_rate:
                            promoted = dataclasses.replace(promoted, stage=ArtifactStage.THEORY)

                    repo.register_artifact(promoted)

                    if promoted.stage == ArtifactStage.TECHNOLOGY:
                        import dataclasses
                        new_rep = ecology_model.calculate_logistic_reputation_gain(org.reputation, 0.25)
                        updated_org = dataclasses.replace(org, reputation=new_rep)
                        manager._snapshots[org.org_id] = updated_org
                        ctx.bus.publish(
                            "ResearchCompletedEvent",
                            ResearchCompletedEvent(org.org_id, promoted.artifact_id, True, float(tick))
                        )


        # 3. Knowledge Memory Decay (accessibility decreases based on citations/citations rate)
        from runtime.science.knowledge_repository import KnowledgeRepository
        try:
            repo = ctx.registry.resolve(KnowledgeRepository)
            all_arts = list(repo.get_all_artifacts())
            for art in all_arts:
                # Calculate citations (how many artifacts list this one as parent)
                citations = sum(1 for a in all_arts if a.parent_artifact_id == art.artifact_id)
                decay_rate = ecology_model.calculate_memory_decay(citations, art.replications)

                # Speciation memory retention multiplier: higher retention reduces memory decay
                # Resolve the organization that owns/produced this artifact
                owning_modifier = None
                for o in manager.get_all_snapshots():
                    if o.stage != OrganizationStage.COLLAPSED:
                        if any(a.artifact_id == art.artifact_id for a in o.collective_memory):
                            owning_modifier = SPECIES_MODIFIERS.get(o.speciation_profile)
                            break
                if owning_modifier is None:
                    from runtime.society.organization import SpeciationModifier
                    owning_modifier = SpeciationModifier(1.0, 1.0, 1.0, 1.0)

                decay_rate = decay_rate / owning_modifier.memory_retention

                
                decayed_acc = max(0.0, art.accessibility - decay_rate)
                updated_art = KnowledgeArtifact(
                    artifact_id=art.artifact_id,
                    title=art.title,
                    stage=art.stage,
                    confidence=art.confidence,
                    replications=art.replications,
                    contradictions=art.contradictions,
                    novelty=art.novelty,
                    author=art.author,
                    parent_artifact_id=art.parent_artifact_id,
                    contributors=art.contributors,
                    created_tick=art.created_tick,
                    accessibility=decayed_acc,
                    niche=art.niche,
                    origin_species=art.origin_species,
                )
                repo.register_artifact(updated_art)
        except KeyError:
            pass

        # 4. Prestige Decay & Decline/Collapse/Recovery/Dormant Lifecycle Loops
        for org in list(manager.get_all_snapshots()):
            if org.stage == OrganizationStage.COLLAPSED:
                continue

            import dataclasses
            # Apply passive prestige decay (accelerated if DORMANT)
            if org.stage == OrganizationStage.DORMANT:
                decayed_rep = max(1.0, org.reputation - 0.05)
            else:
                decayed_rep = ecology_model.apply_prestige_decay(org.reputation)
            org = dataclasses.replace(org, reputation=decayed_rep)
            manager._snapshots[org.org_id] = org

            # Evaluate collapse score
            score = ecology_model.evaluate_collapse_score(org)
            prev_stage = org.stage

            # 20 ticks dormant timer check
            dormant_expired = False
            if prev_stage == OrganizationStage.DORMANT and org.dormant_since_tick is not None:
                if tick - org.dormant_since_tick >= 20:
                    dormant_expired = True

            if score > 0.95 or dormant_expired:
                # Collapse — record fossil before removing from active pool
                try:
                    fossil_svc = ctx.registry.resolve(FossilRecord)
                except KeyError:
                    fossil_svc = FossilRecord()
                    ctx.registry.register(FossilRecord, fossil_svc)

                artifacts_produced = len(org.collective_memory)
                fossil_svc.record_fossil(ExtinctSpeciesRecord(
                    org_id=org.org_id,
                    name=org.name,
                    profile=org.speciation_profile,
                    birth_tick=float(org.created_tick),
                    death_tick=float(tick),
                    peak_fitness=org.reputation,
                    artifacts_produced=artifacts_produced,
                ))

                ext_evt = ExtinctionEvent(
                    org_id=org.org_id,
                    name=org.name,
                    profile=org.speciation_profile,
                    lineage_depth=org.dna.lineage_depth if org.dna else 0,
                    artifacts_count=artifacts_produced,
                    timestamp=float(tick),
                )
                ctx.bus.publish("ExtinctionEvent", ext_evt)

                collapse_evt = OrganizationCollapsedEvent(org.org_id, "extinction", float(tick))
                manager.apply_event(collapse_evt)
                ctx.bus.publish("OrganizationCollapsedEvent", collapse_evt)
            elif score > 0.75:
                # Enter/Stay DORMANT Stage
                if prev_stage != OrganizationStage.DORMANT:
                    org = dataclasses.replace(org, stage=OrganizationStage.DORMANT, dormant_since_tick=tick)
                    manager._snapshots[org.org_id] = org
                    ctx.bus.publish("OrganizationEnteredDormantEvent", {"org_id": org.org_id, "tick": tick})
            elif score > 0.60:
                # Decline or Revival check
                if prev_stage == OrganizationStage.DORMANT:
                    # Reform DNA under Revival Stage (takes 10 ticks)
                    import random
                    rnd = random.Random(tick + hash(org.org_id))
                    fitness_before = org.reputation
                    mutated_cognitive = tuple(
                        max(0.0, min(1.0, val + rnd.uniform(-0.05, 0.05)))
                        for val in org.dna.cognitive_traits
                    ) if org.dna else (0.5, 0.5, 0.5)
                    org = dataclasses.replace(
                        org,
                        stage=OrganizationStage.REVIVAL,
                        revival_until_tick=tick + 10,
                        dna=dataclasses.replace(org.dna, cognitive_traits=mutated_cognitive) if org.dna else None
                    )
                    manager._snapshots[org.org_id] = org
                    ctx.bus.publish("OrganizationEnteredRevivalEvent", {"org_id": org.org_id, "tick": tick})
                    ctx.bus.publish("AdaptationEvent", AdaptationEvent(
                        org_id=org.org_id,
                        fitness_before=fitness_before,
                        fitness_after=org.reputation,
                        trigger="dormant_revival_mutation",
                        timestamp=float(tick),
                    ))
                elif prev_stage == OrganizationStage.REVIVAL:
                    # Stabilize if 10 ticks elapsed
                    if org.revival_until_tick is not None and tick >= org.revival_until_tick:
                        org = dataclasses.replace(org, stage=OrganizationStage.ACTIVE, revival_until_tick=None, dormant_since_tick=None)
                        manager._snapshots[org.org_id] = org
                        ctx.bus.publish("OrganizationRecoveredEvent", {"org_id": org.org_id, "tick": tick})
                elif prev_stage != OrganizationStage.DECLINING:
                    org = dataclasses.replace(org, stage=OrganizationStage.DECLINING)
                    manager._snapshots[org.org_id] = org
                    ctx.bus.publish("OrganizationEnteredDeclineEvent", {"org_id": org.org_id, "tick": tick})
            else:
                # Recover
                if prev_stage == OrganizationStage.DECLINING:
                    org = dataclasses.replace(org, stage=OrganizationStage.ACTIVE)
                    manager._snapshots[org.org_id] = org
                    ctx.bus.publish("OrganizationRecoveredEvent", {"org_id": org.org_id, "tick": tick})
                elif prev_stage == OrganizationStage.DORMANT:
                    import random
                    rnd = random.Random(tick + hash(org.org_id))
                    fitness_before = org.reputation
                    mutated_cognitive = tuple(
                        max(0.0, min(1.0, val + rnd.uniform(-0.05, 0.05)))
                        for val in org.dna.cognitive_traits
                    ) if org.dna else (0.5, 0.5, 0.5)
                    org = dataclasses.replace(
                        org,
                        stage=OrganizationStage.REVIVAL,
                        revival_until_tick=tick + 10,
                        dna=dataclasses.replace(org.dna, cognitive_traits=mutated_cognitive) if org.dna else None
                    )
                    manager._snapshots[org.org_id] = org
                    ctx.bus.publish("OrganizationEnteredRevivalEvent", {"org_id": org.org_id, "tick": tick})
                    ctx.bus.publish("AdaptationEvent", AdaptationEvent(
                        org_id=org.org_id,
                        fitness_before=fitness_before,
                        fitness_after=org.reputation,
                        trigger="dormant_recovery_mutation",
                        timestamp=float(tick),
                    ))
                elif prev_stage == OrganizationStage.REVIVAL:
                    if org.revival_until_tick is not None and tick >= org.revival_until_tick:
                        org = dataclasses.replace(org, stage=OrganizationStage.ACTIVE, revival_until_tick=None, dormant_since_tick=None)
                        manager._snapshots[org.org_id] = org
                        ctx.bus.publish("OrganizationRecoveredEvent", {"org_id": org.org_id, "tick": tick})


        # Sync active organizations list to settlements for metrics tracking
        for civ in world.civilizations:
            for setl in civ.settlements:
                setl.institutions = [o for o in manager.get_all_snapshots() if o.stage != OrganizationStage.COLLAPSED]

        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})
