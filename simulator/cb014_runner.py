"""
CB-014: Scientific Institution Emergence Benchmark.

Conducts A/B test of World A (Solo Agents) vs World B (Institutionalized Agents).
Evaluates Collaboration Rates (RCR), Discovery Velocities (DV),
Collective Intelligence Gain (CIG), and Knowledge Quality Index (KQI).

Usage:
    py simulator/cb014_runner.py --cycles 1000 --seed 42
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
from runtime.observability.metric import MetricContext


# Mock components for decision isolation during A/B baseline
class ForbiddenDecisionPolicy:
    def evaluate_decision(self, utility_eval, risk, exploration):
        return None

    def decide(self, evaluation):
        class RejectResult:
            action = DecisionAction.REJECT if 'DecisionAction' in globals() else "REJECT"
        return RejectResult()


def run_world(cycles: int, seed: int, allow_institutions: bool):
    random.seed(seed)
    config = SimulationConfig(seed=seed)
    # We execute only the science_institution stage
    config.tick_pipeline = ("science_institution",)

    bus = EventBus()
    registry = ServiceRegistry()

    manager = InstitutionManager()
    registry.register(InstitutionManager, manager)

    from runtime.observability.telemetry import CognitiveTelemetry
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

    agents_by_id = {}
    for i in range(100):
        agent_id = f"agent-{i}"
        agent = CognitiveAgent(agent_id)
        agent.resource_budget = ResourceBudget({"energy": 1000, "attention": 100})
        agent.knowledge = 1.0
        agent.utility_func = WeightedLogUtilityFunction()
        agent.world = world

        if not allow_institutions:
            # Inject utility / policy that prevents any group joining
            class SoloUtility:
                def evaluate_join_score(self, agent, org, solo_utility):
                    return -999.0
            agent.utility_func = SoloUtility()

        s1.add_agent(agent)
        agents_by_id[agent.identity.agent_id] = agent

    # Track generated events
    events_log = []
    def log_evt(e, p):
        events_log.append(p)

    bus.subscribe("ResearchStartedEvent", log_evt)
    bus.subscribe("ResearchCompletedEvent", log_evt)
    bus.subscribe("MemberJoinedEvent", log_evt)
    bus.subscribe("MemberLeftEvent", log_evt)
    bus.subscribe("OrganizationCreatedEvent", log_evt)
    bus.subscribe("OrganizationCollapsedEvent", log_evt)

    from runtime.science.knowledge_repository import KnowledgeRepository
    repo = KnowledgeRepository()
    registry.register(KnowledgeRepository, repo)

    sim = Simulation(world, ctx)
    sim.run(cycles=cycles, agents_by_id=agents_by_id)

    artifacts = repo.get_all_artifacts()


    return artifacts, events_log, world, manager


def run_cb014(cycles: int = 100, seed: int = 42):
    # Universe A: Solo baseline
    solo_arts, solo_evts, world_a, manager_a = run_world(cycles, seed, allow_institutions=False)

    # Universe B: Institutional cooperative world
    coop_arts, coop_evts, world_b, manager_b = run_world(cycles, seed, allow_institutions=True)

    # Calculations
    ctx_a = MetricContext(tick=cycles, events=tuple(solo_arts + solo_evts), world_snapshot=world_a)
    ctx_b = MetricContext(tick=cycles, events=tuple(coop_arts + coop_evts), world_snapshot=world_b)

    dv_calc = DiscoveryVelocity()
    dv_a = dv_calc.compute(ctx_a)
    dv_b = dv_calc.compute(ctx_b)

    # CIG (Collective Intelligence Gain) calculation
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
    print(f"IFR:                     {ifr:.4f}")
    print(f"ISR:                     {isr:.4f}")
    print("\nCOLLECTIVE INTELLIGENCE")
    print("-----------------------")
    print(f"CIG:                     {cig:.4f}")
    print(f"KQI:                     {kqi:.4f}")
    print("========================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CB-014 Scientific Institution Benchmark")
    parser.add_argument("--cycles", type=int, default=100)
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()
    run_cb014(cycles=args.cycles, seed=args.seed)
