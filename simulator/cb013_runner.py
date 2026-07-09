"""
CB-013: Emergent Trade & Barter Benchmark.

Demonstrates barter utility exchange between complementary agents
and evaluates Pareto efficiency, Value Creation, and composite CCI.

Usage:
    py simulator/cb013_runner.py --cycles 100 --seed 42
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
from runtime.contracts import SchedulerProtocol, EventBusProtocol
from runtime.observability.telemetry import CognitiveTelemetry
from runtime.civilization.world import World
from runtime.civilization.civilization import Civilization
from runtime.civilization.settlement import Settlement
from runtime.civilization.simulation import Simulation
from runtime.agents.agent import CognitiveAgent
from runtime.economy.resource_budget import ResourceBudget
from runtime.economy.budget_policy import BudgetPolicy

# Emergent trade additions
from runtime.economy.types import ResourceType, KnowledgeArtifactType, TradeItem, AgentId, TradeStatus
from runtime.economy.utility_context import UtilityContext
from runtime.economy.utility_function import WeightedLogUtilityFunction
from runtime.economy.utility_policy import DeltaUtilityPolicy
from runtime.economy.decision_policy import WeightedDecisionPolicy, DecisionAction, DecisionEvaluation
from runtime.social.trade_proposal import TradeProposal
from runtime.social.matching_policy import ScarcityPolicy
from runtime.social.matching_engine import MatchingEngine, TradeOpportunity
from runtime.social.trade_engine import TradeEngine
from runtime.observability.metric import TradeMetricsEvent
from runtime.observability.metrics_registry import MetricRegistry, CCICalculator
from runtime.observability.economic_metrics import (
    ParetoEfficiencyMetric, TradeAcceptanceMetric, NegotiationDepthMetric,
    ValueCreationMetric, AverageCreatedValueMetric, EconomicIndexMetric, KnowledgeIndexMetric
)


# ─── Custom Pipeline Stages for Barter Sim ────────────────────────────────────

class BarterMatchingStage:
    name = "plan"  # Replaces 'plan' phase in the pipeline

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        engine = ctx.registry.resolve(MatchingEngine)
        trade_engine = ctx.registry.resolve(TradeEngine)
        
        agents = state.get("agents_by_id", {})
        tick = state.get("current_tick", 0)

        opps = engine.find_opportunities(agents, ctx=None)
        
        # Keep track of active negotiations to avoid duplicate proposals
        active_props = state.setdefault("active_proposals", [])

        for opp in opps:
            # Check if there is already an active proposal between these agents
            if any(p.from_agent == opp.from_agent_id and p.to_agent == opp.to_agent_id for p in active_props):
                continue
            
            # Formulate initial trade offer: propose swapping 10 units of excess for 5 units of requested
            offer = (TradeItem(opp.offered_resource, 10.0),)
            request = (TradeItem(opp.requested_resource, 5.0),)

            prop = trade_engine.propose(
                from_agent_id=opp.from_agent_id,
                to_agent_id=opp.to_agent_id,
                offer=offer,
                request=request,
                tick=tick
            )
            active_props.append(prop)

        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class BarterTradeStage:
    name = "communicate"  # Replaces 'communicate' phase in the pipeline

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        trade_engine = ctx.registry.resolve(TradeEngine)
        agents = state.get("agents_by_id", {})
        active_props = state.get("active_proposals", [])
        tick = state.get("current_tick", 0)

        resolved_props = []
        for prop in list(active_props):
            if prop.status not in (TradeStatus.PROPOSED, TradeStatus.COUNTER):
                continue

            receiver = agents.get(prop.to_agent)
            if not receiver:
                continue

            # Build mock counterpart state for evaluation
            sender = agents.get(prop.from_agent)
            utility_ctx = UtilityContext(current_tick=tick, environment=world.environment, counterpart=sender)
            
            # Predict utility change if trade is executed
            # Calculate utility delta for receiver (reversing offer/request resources)
            # Receiver deducts proposal.request (from receiver perspective) and receives proposal.offer
            # Let's create a temporary mock of B's state before and after:
            b_before = receiver
            b_after = type("MockB", (object,), {
                "resource_budget": ResourceBudget({
                    "energy": float(receiver.resource_budget.balances.get("energy", 0.0)) + (prop.offer[0].amount if prop.offer[0].resource_type == ResourceType.ENERGY else 0.0) - (prop.request[0].amount if prop.request[0].resource_type == ResourceType.ENERGY else 0.0),
                    "attention": float(receiver.resource_budget.balances.get("attention", 0.0)) + (prop.offer[0].amount if prop.offer[0].resource_type == ResourceType.ATTENTION else 0.0) - (prop.request[0].amount if prop.request[0].resource_type == ResourceType.ATTENTION else 0.0),
                }),
                "knowledge": float(receiver.knowledge) + (prop.offer[0].amount if prop.offer[0].resource_type == KnowledgeArtifactType.KNOWLEDGE else 0.0) - (prop.request[0].amount if prop.request[0].resource_type == KnowledgeArtifactType.KNOWLEDGE else 0.0),
                "trust_score": receiver.trust_score
            })()

            policy_util = DeltaUtilityPolicy(receiver.utility_func)
            util_eval = policy_util.delta(b_before, b_after, utility_ctx)
            
            # Make trade decision
            policy_dec = receiver.decision_policy
            dec_eval = policy_dec.evaluate_decision(util_eval, risk=0.0, exploration=0.0)
            dec_res = policy_dec.decide(dec_eval)

            # TradeEngine processes decision
            updated_prop = trade_engine.evaluate_proposal(prop, dec_res, tick)
            
            # Replace in active proposals
            active_props.remove(prop)
            if updated_prop.status in (TradeStatus.ACCEPTED, TradeStatus.COUNTER):
                active_props.append(updated_prop)

        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class BarterExecutionStage:
    name = "execute"  # Replaces 'execute' phase in the pipeline

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        trade_engine = ctx.registry.resolve(TradeEngine)
        agents = state.get("agents_by_id", {})
        active_props = state.get("active_proposals", [])
        tick = state.get("current_tick", 0)

        world.tick(ctx)

        for prop in list(active_props):
            if prop.status == TradeStatus.ACCEPTED:
                sender = agents.get(prop.from_agent)
                receiver = agents.get(prop.to_agent)
                
                success = trade_engine.commit_and_execute(prop, sender, receiver, tick)
                if success:
                    active_props.remove(prop)

        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


# ─── Runner Logic ─────────────────────────────────────────────────────────────

def run_benchmark(cycles: int = 100, seed: int = 42):
    random.seed(seed)
    
    # 1. Config & Context
    config = SimulationConfig(seed=seed)
    bus = EventBus()
    registry = ServiceRegistry()
    telemetry = CognitiveTelemetry()
    telemetry.attach_to_bus(bus)

    # Register Metrics
    metric_registry = MetricRegistry()
    metric_registry.register_metric(EconomicIndexMetric())
    metric_registry.register_metric(KnowledgeIndexMetric())
    metric_registry.register_metric(ParetoEfficiencyMetric())
    metric_registry.register_metric(TradeAcceptanceMetric())
    metric_registry.register_metric(NegotiationDepthMetric())
    metric_registry.register_metric(ValueCreationMetric())
    metric_registry.register_metric(AverageCreatedValueMetric())

    # Direct push integration
    bus.subscribe("ProposalCreated", lambda e, p: metric_registry.log_event(p))
    bus.subscribe("CounterCreated", lambda e, p: metric_registry.log_event(p))
    bus.subscribe("Accepted", lambda e, p: metric_registry.log_event(p))
    bus.subscribe("TradeMetricsEvent", lambda e, p: metric_registry.log_event(p))

    cci_calc = CCICalculator(metric_registry)

    ctx = RuntimeContext(bus=bus, registry=registry, clock=None, telemetry=telemetry, config=config)

    # Register trade engine and matcher
    trade_engine = TradeEngine(event_bus=bus)
    matching_engine = MatchingEngine(ScarcityPolicy())
    
    registry.register(TradeEngine, trade_engine)
    registry.register(MatchingEngine, matching_engine)

    # Override pipeline stages for barter
    registry.register_stage("plan", BarterMatchingStage())
    registry.register_stage("communicate", BarterTradeStage())
    registry.register_stage("execute", BarterExecutionStage())

    # 2. Setup World & Complementary Barter Agents
    world = World("Barter-World")
    civ = Civilization("Barter-Civ")
    world.add_civilization(civ)

    agents_by_id = {}
    
    # Agent A: High energy, low attention (needs attention)
    a1 = CognitiveAgent("Agent-A")
    a1.resource_budget = ResourceBudget({"energy": 1000, "attention": 5})
    a1.knowledge = 1.0
    a1.utility_func = WeightedLogUtilityFunction(w_energy=1.0, w_knowledge=0.5, w_trust=0.0)
    a1.decision_policy = WeightedDecisionPolicy(w_util=1.0, w_risk=0.0, w_exp=0.0)
    
    # Agent B: Low energy, high attention (needs energy)
    a2 = CognitiveAgent("Agent-B")
    a2.resource_budget = ResourceBudget({"energy": 50, "attention": 50})
    a2.knowledge = 2.0
    a2.utility_func = WeightedLogUtilityFunction(w_energy=3.0, w_knowledge=0.5, w_trust=0.0)
    a2.decision_policy = WeightedDecisionPolicy(w_util=1.0, w_risk=0.0, w_exp=0.0)

    # Agent C: Moderate balance
    a3 = CognitiveAgent("Agent-C")
    a3.resource_budget = ResourceBudget({"energy": 300, "attention": 25})
    a3.knowledge = 1.5
    a3.utility_func = WeightedLogUtilityFunction(w_energy=1.0, w_knowledge=1.0, w_trust=0.0)
    a3.decision_policy = WeightedDecisionPolicy(w_util=1.0, w_risk=0.0, w_exp=0.0)

    # Add to world structures
    s1 = Settlement("Settlement-Alpha")
    s1.add_agent(a1)
    s1.add_agent(a2)
    s1.add_agent(a3)
    civ.add_settlement(s1)

    agents_by_id[a1.identity.agent_id] = a1
    agents_by_id[a2.identity.agent_id] = a2
    agents_by_id[a3.identity.agent_id] = a3

    # Add back-references for mocks
    a1.world = world
    a2.world = world
    a3.world = world

    # 3. Execute Simulation
    sim = Simulation(world, ctx)
    snapshot = sim.run(cycles=cycles, agents_by_id=agents_by_id)

    # 4. Compute Final Metrics
    metrics_vals = metric_registry.compute_all(cycles, world)
    final_cci = cci_calc.calculate_cci(cycles, world)

    per = metrics_vals.get("pareto_efficiency_ratio", 1.0)
    tar = metrics_vals.get("trade_acceptance_ratio", 0.0)
    nd  = metrics_vals.get("negotiation_depth", 0.0)
    vcr = metrics_vals.get("value_creation_ratio", 0.0)
    acv = metrics_vals.get("average_created_value", 0.0)

    # Count actual executions in trade history
    trades_executed = len([e for e in trade_engine.history.get_events() if e.event_type == "Executed"])
    trades_proposed = len([e for e in trade_engine.history.get_events() if e.event_type == "ProposalCreated"])

    print("========================================")
    print(" CB-013 EMERGENT TRADE BENCHMARK")
    print("========================================")
    print(f"Agents:                  {len(agents_by_id)}")
    print(f"Trades proposed:         {trades_proposed}")
    print(f"Trades executed:         {trades_executed}")
    print(f"Acceptance Ratio (TAR):  {tar:.2f}")
    print(f"Pareto Efficiency (PER): {per:.2f}")
    print(f"Negotiation Depth (ND):  {nd:.1f}")
    print(f"Value Creation (VCR):    {vcr:.2f}")
    print(f"Average Created Val (ACV): {acv:.4f}")
    print(f"CCI:                     {final_cci:.4f}")
    print("========================================")

    return {
        "trades_proposed": trades_proposed,
        "trades_executed": trades_executed,
        "tar": tar,
        "per": per,
        "nd": nd,
        "vcr": vcr,
        "cci": final_cci
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CB-013 Emergent Trade Barter Benchmark")
    parser.add_argument("--cycles", type=int, default=100)
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()
    run_benchmark(cycles=args.cycles, seed=args.seed)
