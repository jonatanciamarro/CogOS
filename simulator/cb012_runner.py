"""
CB-012: Long-Duration Civilization Stability Benchmark.

Usage:
    py simulator/cb012_runner.py                    # 100 cycles (default)
    py simulator/cb012_runner.py --cycles 10        # CI fast mode
    py simulator/cb012_runner.py --cycles 1000 --seed 42  # stability test
"""
import sys
import os
import argparse
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.bus.event_bus import EventBus, CogOSEvents, EventPriority
from runtime.config.simulation_config import SimulationConfig
from runtime.context.runtime_context import RuntimeContext
from runtime.context.service_registry import ServiceRegistry
from runtime.contracts import SchedulerProtocol, EconomyProtocol
from runtime.economy.resource_scheduler import ResourceScheduler
from runtime.economy.scheduling_policy import ScientificPolicy
from runtime.economy.budget_policy import BudgetPolicy
from runtime.economy.resource_budget import ResourceBudget
from runtime.economy.market import IdeaMarket
from runtime.observability.telemetry import CognitiveTelemetry
from runtime.civilization.world import World
from runtime.civilization.civilization import Civilization
from runtime.civilization.settlement import Settlement
from runtime.civilization.simulation_loop import SimulationLoop
from runtime.agents.agent import CognitiveAgent


def build_context(config: SimulationConfig) -> RuntimeContext:
    random.seed(config.seed)
    bus = EventBus()
    registry = ServiceRegistry()
    telemetry = CognitiveTelemetry()
    telemetry.attach_to_bus(bus)

    registry.register(SchedulerProtocol, ResourceScheduler(policy=ScientificPolicy()))

    market = IdeaMarket(idle_sweep_threshold=config.idle_sweep_threshold)
    registry.register(EconomyProtocol, market)

    return RuntimeContext(bus=bus, registry=registry, clock=None,
                         telemetry=telemetry, config=config)


def build_world(ctx: RuntimeContext, agent_count: int = 5) -> tuple:
    world = World("CogOS-CB012")
    civ = Civilization("Alpha")
    agents_by_id = {}

    for i, name in enumerate(["Researcher", "Replicator", "Explorer", "Analyst", "Pioneer"][:agent_count]):
        s = Settlement(f"Settlement-{i}")
        agent = CognitiveAgent(name)
        agent.resource_budget = ResourceBudget(
            BudgetPolicy.for_role("founder" if i == 0 else "standard")
        )
        agent.trust_score = 0.5 + i * 0.05
        s.add_agent(agent)
        civ.add_settlement(s)
        agents_by_id[agent.identity.agent_id] = agent

    # Register hypotheses in IdeaMarket
    market = ctx.registry.resolve(EconomyProtocol)
    for h_id in ["hyp/gravity", "hyp/dark_energy", "hyp/consciousness"]:
        entry = market.register_hypothesis(h_id)
        entry.eig = round(random.uniform(0.4, 0.9), 2)
        entry.impact_expected = round(random.uniform(0.3, 0.8), 2)
        entry.risk = round(random.uniform(0.1, 0.5), 2)

    world.add_civilization(civ)
    return world, agents_by_id, market


def run_benchmark(cycles: int = 100, seed: int = 42, agent_count: int = 5):
    config = SimulationConfig(seed=seed)
    ctx = build_context(config)
    world, agents_by_id, market = build_world(ctx, agent_count)

    # Metric counters via EventBus
    epochs_seen    = [0]
    budget_events  = [0]
    publications   = [0]

    ctx.bus.subscribe(CogOSEvents.EPOCH_ADVANCED,
                      lambda e, p: epochs_seen.__setitem__(0, epochs_seen[0]+1),
                      EventPriority.HIGH)
    ctx.bus.subscribe(CogOSEvents.BUDGET_EXHAUSTED,
                      lambda e, p: budget_events.__setitem__(0, budget_events[0]+1),
                      EventPriority.CRITICAL)
    ctx.bus.subscribe(CogOSEvents.PUBLICATION_ACCEPTED,
                      lambda e, p: publications.__setitem__(0, publications[0]+1),
                      EventPriority.NORMAL)

    loop = SimulationLoop(world, ctx)
    snapshot = loop.run(cycles=cycles, agents_by_id=agents_by_id, idea_market=market)

    # Compute metrics
    kar = publications[0] / max(1, epochs_seen[0])      # Knowledge Accumulation Rate
    avg_trust = sum(a.trust_score for a in agents_by_id.values()) / max(1, len(agents_by_id))
    resource_pool = world.civilizations[0].environment.get_system("ResourcePool")
    rs_energy = resource_pool.energy if resource_pool else 0

    ranked = market.rank_by_evi()
    top_id, top_evi = ranked[0] if ranked else ("n/a", 0)

    print("=============================================")
    print(f"  CB-012 BENCHMARK — {cycles} cycles, seed={seed}")
    print("=============================================")
    print(f"  Epochs completed:              {epochs_seen[0]}")
    print(f"  Knowledge Accumulation Rate:   {kar:.3f}")
    print(f"  Avg Agent Trust (AFT proxy):   {avg_trust:.3f}")
    print(f"  ResourcePool energy (RS):      {rs_energy}")
    print(f"  Budget Exhaustions:            {budget_events[0]}")
    print(f"  Top Hypothesis by EVI:         {top_id} ({top_evi:.4f})")
    print(f"  Telemetry buffer size:         {snapshot['buffer_size']}")
    print("=============================================")

    return {"kar": kar, "avg_trust": avg_trust, "rs_energy": rs_energy,
            "budget_exhaustions": budget_events[0], "epochs": epochs_seen[0]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CB-012 Civilization Stability Benchmark")
    parser.add_argument("--cycles", type=int, default=100)
    parser.add_argument("--seed",   type=int, default=42)
    parser.add_argument("--agents", type=int, default=5)
    args = parser.parse_args()
    run_benchmark(cycles=args.cycles, seed=args.seed, agent_count=args.agents)
