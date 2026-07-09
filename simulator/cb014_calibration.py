"""
CB-014: Scientific Institution Stress & Calibration Benchmark.

Executes calibration scenarios:
1. High competition/coordination friction.
2. Knowledge memory decay (reduced accessibility).
3. Black Swan resource shocks (90% global energy reduction).

Usage:
    py simulator/cb014_calibration.py --cycles 200 --seed 42
"""
import sys
import os
import argparse
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.bus.event_bus import EventBus
from runtime.config.simulation_config import SimulationConfig
from runtime.context.runtime_context import RuntimeContext
from runtime.context.service_registry import ServiceRegistry
from runtime.civilization.world import World
from runtime.civilization.civilization import Civilization
from runtime.civilization.settlement import Settlement
from runtime.civilization.simulation import Simulation
from runtime.agents.agent import CognitiveAgent
from runtime.economy.types import AgentId
from runtime.economy.resource_budget import ResourceBudget
from runtime.economy.utility_function import WeightedLogUtilityFunction
from runtime.society.organization import OrganizationStage
from runtime.society.institution_manager import InstitutionManager
from runtime.pipeline.science_institution_stage import ScienceInstitutionStage
from runtime.observability.scientific_metrics import (
    ResearchCollaborationRate, DiscoveryVelocity, KnowledgeTransferEfficiency,
    InstitutionFormationRate, InstitutionSurvivalRate, KnowledgeQualityIndex
)
from runtime.observability.stress_metrics import (
    CollectiveBureaucracyIndex, InstitutionalSweetSpot, AdaptiveResilienceScore, KnowledgeRetentionTime
)
from runtime.observability.ecology_metrics import (
    InstitutionChurnRate, InstitutionalHalfLife, InstitutionalRecoveryIndex, InstitutionDiversityIndex
)


from runtime.observability.metric import MetricContext
from runtime.observability.telemetry import CognitiveTelemetry
from runtime.science.knowledge_repository import KnowledgeRepository



def run_world(cycles: int, seed: int, allow_institutions: bool):
    random.seed(seed)
    config = SimulationConfig(seed=seed)
    config.tick_pipeline = ("science_institution",)

    bus = EventBus()
    registry = ServiceRegistry()

    manager = InstitutionManager()
    registry.register(InstitutionManager, manager)

    telemetry = CognitiveTelemetry()
    telemetry.attach_to_bus(bus)

    ctx = RuntimeContext(bus=bus, registry=registry, clock=None, telemetry=telemetry, config=config)

    science_stage = ScienceInstitutionStage()
    registry.register_stage("science_institution", science_stage)

    world = World("CB-014-World")
    civ = Civilization("Civ")
    world.add_civilization(civ)
    s1 = Settlement("Settlement-Alpha")
    civ.add_settlement(s1)

    repo = KnowledgeRepository()
    registry.register(KnowledgeRepository, repo)

    agents_by_id = {}
    for i in range(100):
        agent_id = f"agent-{i}"
        agent = CognitiveAgent(agent_id)
        agent.resource_budget = ResourceBudget({"energy": 1000, "attention": 100})
        agent.knowledge = 1.0
        agent.utility_func = WeightedLogUtilityFunction()
        agent.world = world

        if not allow_institutions:
            class SoloUtility:
                def evaluate_join_score(self, agent, org, solo_utility):
                    return -999.0
            agent.utility_func = SoloUtility()

        s1.add_agent(agent)
        agents_by_id[agent.identity.agent_id] = agent

    sim = Simulation(world, ctx)
    sim.run(cycles=cycles, agents_by_id=agents_by_id)

    return repo.get_all_artifacts(), [], world, manager


def run_stress_sim(cycles: int, seed: int, apply_shock: bool):
    random.seed(seed)
    config = SimulationConfig(seed=seed)
    config.tick_pipeline = ("science_institution",)

    bus = EventBus()
    registry = ServiceRegistry()

    manager = InstitutionManager()
    registry.register(InstitutionManager, manager)

    telemetry = CognitiveTelemetry()
    telemetry.attach_to_bus(bus)

    ctx = RuntimeContext(bus=bus, registry=registry, clock=None, telemetry=telemetry, config=config)

    science_stage = ScienceInstitutionStage()
    registry.register_stage("science_institution", science_stage)

    world = World("CB-014-World")
    civ = Civilization("Civ")
    world.add_civilization(civ)
    s1 = Settlement("Settlement-Alpha")
    civ.add_settlement(s1)

    repo = KnowledgeRepository()
    registry.register(KnowledgeRepository, repo)

    agents_by_id = {}
    for i in range(100):
        agent_id = f"agent-{i}"
        agent = CognitiveAgent(agent_id)
        agent.resource_budget = ResourceBudget({"energy": 1000, "attention": 100})
        agent.knowledge = 1.0
        agent.utility_func = WeightedLogUtilityFunction()
        agent.world = world
        s1.add_agent(agent)
        agents_by_id[agent.identity.agent_id] = agent

    events_log = []
    def log_evt(e, p):
        events_log.append(p)

    bus.subscribe("ResearchStartedEvent", log_evt)
    bus.subscribe("ResearchCompletedEvent", log_evt)
    bus.subscribe("MemberJoinedEvent", log_evt)
    bus.subscribe("MemberLeftEvent", log_evt)
    bus.subscribe("OrganizationCreatedEvent", log_evt)
    bus.subscribe("OrganizationCollapsedEvent", log_evt)

    sim = Simulation(world, ctx)
    pipeline = sim._build_pipeline(agents_by_id, None)
    sim.kernel.start()

    for tick in range(1, cycles + 1):
        if apply_shock and tick == 50:
            # Black Swan Shock: Global catastrophe draining 90% of resources
            for agent in agents_by_id.values():
                curr_energy = agent.resource_budget.balances.get("energy", 0.0)
                curr_att = agent.resource_budget.balances.get("attention", 0.0)
                agent.resource_budget.consume("energy", int(curr_energy * 0.90))
                agent.resource_budget.consume("attention", int(curr_att * 0.90))
            
            for org in manager.get_all_snapshots():
                curr_org_energy = org.resources.balances.get("energy", 0.0)
                curr_org_att = org.resources.balances.get("attention", 0.0)
                org.resources.consume("energy", int(curr_org_energy * 0.90))
                org.resources.consume("attention", int(curr_org_att * 0.90))

        pipeline.run(tick)

    sim.kernel.stop()
    return repo.get_all_artifacts(), events_log, world, manager


def run_calibration(cycles: int = 200, seed: int = 42):
    # Run Solo baseline
    solo_arts, solo_evts, world_a, manager_a = run_world(cycles, seed, allow_institutions=False)

    # Run Cooperative Stress loop with Shock
    coop_arts, coop_evts, world_b, manager_b = run_stress_sim(cycles, seed, apply_shock=True)

    # Calculations
    ctx_a = MetricContext(tick=cycles, events=tuple(solo_arts + solo_evts), world_snapshot=world_a)
    ctx_b = MetricContext(tick=cycles, events=tuple(coop_arts + coop_evts), world_snapshot=world_b)

    dv_calc = DiscoveryVelocity()
    dv_a = dv_calc.compute(ctx_a)
    dv_b = dv_calc.compute(ctx_b)

    cig = dv_b / dv_a if dv_a > 0.0 else (2.0 if dv_b > 0.0 else 1.0)

    rcr_calc = ResearchCollaborationRate()
    rcr = rcr_calc.compute(ctx_b)

    kte_calc = KnowledgeTransferEfficiency()
    kte = kte_calc.compute(ctx_b)

    ifr_calc = InstitutionFormationRate()
    ifr = ifr_calc.compute(ctx_b)

    isr_calc = InstitutionSurvivalRate()
    isr = isr_calc.compute(ctx_b)

    kqi_calc = KnowledgeQualityIndex()
    kqi = kqi_calc.compute(ctx_b)

    cbi_calc = CollectiveBureaucracyIndex()
    cbi = cbi_calc.compute(ctx_b)

    ars_calc = AdaptiveResilienceScore()
    ars = ars_calc.compute(ctx_b)

    icr_calc = InstitutionChurnRate()
    icr = icr_calc.compute(ctx_b)

    ihl_calc = InstitutionalHalfLife()
    ihl = ihl_calc.compute(ctx_b)

    iri_calc = InstitutionalRecoveryIndex()
    iri = iri_calc.compute(ctx_b)

    idi_calc = InstitutionDiversityIndex()
    idi = idi_calc.compute(ctx_b)

    orgs_created = len([e for e in coop_evts if "OrganizationCreated" in e.__class__.__name__])
    active_orgs = len([o for o in manager_b.get_all_snapshots() if o.stage != OrganizationStage.COLLAPSED])

    print("========================================")
    print(" CB-014 SCIENTIFIC INSTITUTION BENCHMARK")
    print("========================================")
    print("Agents:                  100")
    print(f"Cycles:                  {cycles}")
    print("\nSOLO BASELINE")
    print("-------------")
    print(f"Discoveries:             {len(solo_arts)}")
    print(f"DV:                      {dv_a:.4f}")
    print("\nINSTITUTIONAL WORLD")
    print("-------------------")
    print(f"Organizations:           {orgs_created}")
    print(f"Stable Organizations:    {active_orgs}")
    print(f"RCR:                     {rcr:.4f}")
    print(f"KTE:                     {kte:.4f}")
    print(f"DV:                      {dv_b:.4f}")
    print(f"IFR:                      {ifr:.4f}")
    print(f"ISR:                     {isr:.4f}")
    print(f"ICR:                     {icr:.4f}")
    print(f"IHL:                     {ihl:.1f} ticks")
    print(f"IDI:                     {idi:.4f}")
    print("\nCOLLECTIVE INTELLIGENCE")
    print("-----------------------")
    print(f"CIG:                     {cig:.4f}")
    print(f"KQI:                     {kqi:.4f}")
    print(f"CBI:                     {cbi:.4f}")
    print(f"ARS:                     {ars:.4f}")
    print(f"IRI:                     {iri:.4f}")
    print("========================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CB-014 Calibration & Stress Benchmark")
    parser.add_argument("--cycles", type=int, default=200)
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()
    run_calibration(cycles=args.cycles, seed=args.seed)
