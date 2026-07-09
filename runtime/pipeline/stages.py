"""
runtime/pipeline/stages.py

All tick-cycle stages for CogOS Simulation.
Each stage is an independent object implementing PipelineStage (Protocol).
Simulation.run() never contains domain logic — it only iterates registered stages.

To add a new stage in any Sprint:
    1. Define class MyStage with .name and .run(ctx, world, state)
    2. registry.register_stage("my_stage", MyStage())
    3. Append "my_stage" to SimulationConfig.tick_pipeline
    No other file changes required.
"""
from typing import Protocol, runtime_checkable


# ─── Protocol ──────────────────────────────────────────────────────────────────

@runtime_checkable
class PipelineStage(Protocol):
    """
    PipelineStage is the atomic unit of the simulation tick cycle.
    Each stage runs in the order defined by SimulationConfig.tick_pipeline.
    """
    name: str

    def run(self, ctx, world, state: dict) -> None:
        """
        Execute this stage.

        Args:
            ctx:   RuntimeContext — immutable infrastructure
            world: World — shared space with all civilizations
            state: mutable dict shared across stages within one tick
                   (e.g. agents_by_id, idea_market, current_tick)
        """
        ...


# ─── Concrete stages ───────────────────────────────────────────────────────────

class ObserveStage:
    name = "observe"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        agents = state.get("agents_by_id", {})
        for agent in agents.values():
            if hasattr(agent, "observe"):
                agent.observe(world.environment)
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class PlanStage:
    name = "plan"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.1: agents consult IdeaMarket + WorldModel to form plans
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class AllocateResourcesStage:
    name = "allocate_resources"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        from runtime.contracts import SchedulerProtocol
        try:
            scheduler = ctx.registry.resolve(SchedulerProtocol)
            agents = list(state.get("agents_by_id", {}).values())
            scheduler.allocate_cpu_slice(agents, total_cpu=5000)
        except KeyError:
            pass
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class ExecuteStage:
    name = "execute"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        world.tick(ctx)
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class CommunicateStage:
    name = "communicate"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.1: agents broadcast memes and hypotheses via EventBus
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class LearnStage:
    name = "learn"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.1: agents update WorldModel from observations
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class ScienceStage:
    name = "science"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        market = state.get("idea_market")
        if market:
            market.tick_idle(ctx.bus)
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class CultureStage:
    name = "culture"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.2: cultural selection and meme propagation
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class GovernanceStage:
    name = "governance"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.3: institutional decisions and policy updates
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class EnvironmentUpdateStage:
    name = "environment_update"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        world.environment.tick_local(ctx)
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class HistoryStage:
    name = "history"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        # Sprint 5.X: log epoch snapshot to CivilizationMemory
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


class TelemetryStage:
    name = "telemetry"

    def run(self, ctx, world, state: dict) -> None:
        ctx.bus.publish("PHASE_STARTED", {"phase": self.name})
        from runtime.cogos.resource_daemon import ResourceDaemon
        daemon = state.get("daemon")
        if daemon:
            daemon.tick(state.get("agents_by_id", {}), state.get("idea_market"))
        ctx.bus.publish("PHASE_FINISHED", {"phase": self.name})


# ─── Default stage set ─────────────────────────────────────────────────────────

ALL_STAGES = [
    ObserveStage(),
    PlanStage(),
    AllocateResourcesStage(),
    ExecuteStage(),
    CommunicateStage(),
    LearnStage(),
    ScienceStage(),
    CultureStage(),
    GovernanceStage(),
    EnvironmentUpdateStage(),
    HistoryStage(),
    TelemetryStage(),
]


def register_default_stages(registry) -> None:
    """Register all default stages into a ServiceRegistry. Call at bootstrap."""
    for stage in ALL_STAGES:
        registry.register_stage(stage.name, stage)
