from runtime.civilization.simulation_kernel import SimulationKernel, KernelState
from runtime.cogos.resource_daemon import ResourceDaemon
from runtime.bus.event_bus import CogOSEvents, EventPriority


class TickPipeline:
    """
    TickPipeline executes one simulation tick as an ordered sequence of named phases.
    Phase order comes from SimulationConfig.tick_pipeline — resolved via ServiceRegistry.
    """
    def __init__(self, context, world, agents_by_id: dict, idea_market=None, daemon=None):
        self.ctx = context
        self.world = world
        self.state = {
            "agents_by_id": agents_by_id,
            "idea_market": idea_market,
            "daemon": daemon,
        }

    def run(self, tick: int) -> None:
        self.state["current_tick"] = tick
        for phase_name in self.ctx.config.tick_pipeline:
            stage = self.ctx.registry.resolve_stage(phase_name)
            if stage:
                stage.run(self.ctx, self.world, self.state)


class Simulation:
    """
    Simulation is the root orchestrator — sits above World in the hierarchy.

    Hierarchy:
        Simulation
        └── World
            └── Civilization
                └── Settlement
                    └── Agent

    Responsibilities of Simulation (NOT World):
        - SimulationKernel (state machine)
        - TickPipeline (phase ordering)
        - Seed / snapshot / replay
        - Stop criteria
    """
    def __init__(self, world, context):
        self.world = world
        self.ctx = context
        self.kernel = SimulationKernel()
        self._daemon = ResourceDaemon(
            event_bus=context.bus,
            energy_replenish=context.config.energy_regeneration,
            memory_replenish=context.config.memory_regeneration,
        )
        # Register default stages if they are not already registered in context registry
        from runtime.pipeline.stages import ALL_STAGES
        for stage in ALL_STAGES:
            if not self.ctx.registry.resolve_stage(stage.name):
                self.ctx.registry.register_stage(stage.name, stage)

    def _build_pipeline(self, agents_by_id, idea_market):
        return TickPipeline(self.ctx, self.world, agents_by_id, idea_market, self._daemon)

    def run(self, cycles: int, agents_by_id: dict = None, idea_market=None) -> dict:
        """
        Runs the simulation for `cycles` ticks.
        Phase order is defined by ctx.config.tick_pipeline.
        Returns telemetry snapshot.
        """
        agents_by_id = agents_by_id or {}
        pipeline = self._build_pipeline(agents_by_id, idea_market)
        self.kernel.start()

        for _ in range(cycles):
            if not self.kernel.running:
                break
            try:
                tick = self.kernel.tick()
                pipeline.run(tick)
            except Exception as e:
                self.kernel.fail(str(e))
                break

        self.kernel.stop()
        return self.ctx.telemetry.snapshot()
