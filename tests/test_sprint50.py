import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.contracts import (
    IdentityProvider, BudgetProvider, TrustProvider,
    Observable, SchedulerProtocol, EventBusProtocol, TelemetryProtocol
)
from runtime.context.service_registry import ServiceRegistry
from runtime.context.runtime_context import RuntimeContext
from runtime.config.simulation_config import SimulationConfig
from runtime.bus.event_bus import EventBus
from runtime.observability.telemetry import CognitiveTelemetry
from runtime.economy.resource_scheduler import ResourceScheduler
from runtime.civilization.simulation_kernel import SimulationKernel, KernelState
from runtime.civilization.world import World
from runtime.civilization.civilization import Civilization
from runtime.civilization.settlement import Settlement
from runtime.agents.agent import CognitiveAgent
from runtime.economy.resource_budget import ResourceBudget
from runtime.economy.budget_policy import BudgetPolicy


class TestContracts(unittest.TestCase):

    def test_cognitive_agent_satisfies_identity_provider(self):
        agent = CognitiveAgent("Test")
        self.assertIsInstance(agent, IdentityProvider)

    def test_cognitive_agent_satisfies_budget_provider(self):
        agent = CognitiveAgent("Test")
        agent.resource_budget = ResourceBudget(BudgetPolicy.STANDARD)
        self.assertIsInstance(agent, BudgetProvider)

    def test_cognitive_agent_satisfies_trust_provider(self):
        agent = CognitiveAgent("Test")
        self.assertIsInstance(agent, TrustProvider)

    def test_event_bus_satisfies_protocol(self):
        bus = EventBus()
        self.assertIsInstance(bus, EventBusProtocol)

    def test_event_bus_publish_async(self):
        import time
        bus = EventBus()
        result = []
        bus.subscribe("ASYNC_EVT", lambda e, p: result.append(p))
        future = bus.publish_async("ASYNC_EVT", {"val": "async_payload"})
        self.assertIsNotNone(future)
        future.result(timeout=1.0) # Wait for execution
        self.assertEqual(result[0]["val"], "async_payload")
        self.assertIn("sequence_number", result[0])

    def test_event_bus_sequence_number(self):
        from runtime.bus.event_envelope import EventEnvelope
        bus = EventBus()
        payloads = []
        bus.subscribe("SEQ_EVT", lambda e, p: payloads.append(p))
        
        bus.publish("SEQ_EVT", {"data": 1})
        env = EventEnvelope(event_type="SEQ_EVT", payload={"data": 2})
        bus.publish("SEQ_EVT", env)

        self.assertEqual(payloads[0]["sequence_number"], 1)
        self.assertEqual(payloads[1].sequence_number, 2)

    def test_telemetry_satisfies_protocol(self):
        t = CognitiveTelemetry()
        self.assertIsInstance(t, TelemetryProtocol)

    def test_resource_scheduler_satisfies_protocol(self):
        sched = ResourceScheduler()
        self.assertIsInstance(sched, SchedulerProtocol)


class TestServiceRegistry(unittest.TestCase):

    def test_register_and_resolve(self):
        registry = ServiceRegistry()
        from runtime.economy.scheduling_policy import GreedyPolicy
        from runtime.contracts import SchedulerProtocol
        policy = GreedyPolicy()
        registry.register(SchedulerProtocol, policy)
        resolved = registry.resolve(SchedulerProtocol)
        self.assertIs(resolved, policy)

    def test_resolve_missing_raises(self):
        registry = ServiceRegistry()
        from runtime.contracts import ScienceProtocol
        with self.assertRaises(KeyError):
            registry.resolve(ScienceProtocol)

    def test_hot_swap(self):
        registry = ServiceRegistry()
        from runtime.contracts import SchedulerProtocol
        from runtime.economy.scheduling_policy import GreedyPolicy, ScientificPolicy
        registry.register(SchedulerProtocol, GreedyPolicy())
        registry.register(SchedulerProtocol, ScientificPolicy())  # replace
        resolved = registry.resolve(SchedulerProtocol)
        self.assertIsInstance(resolved, ScientificPolicy)


class TestRuntimeContext(unittest.TestCase):

    def _make_context(self):
        bus = EventBus()
        registry = ServiceRegistry()
        telemetry = CognitiveTelemetry()
        config = SimulationConfig()
        return RuntimeContext(bus=bus, registry=registry, clock=None,
                              telemetry=telemetry, config=config)

    def test_context_is_frozen(self):
        ctx = self._make_context()
        with self.assertRaises(Exception):
            ctx.bus = None  # frozen=True prevents mutation

    def test_context_carries_config(self):
        ctx = self._make_context()
        self.assertEqual(ctx.config.ticks_per_epoch, 50)


class TestSimulationKernel(unittest.TestCase):

    def test_boot_to_running(self):
        k = SimulationKernel()
        self.assertEqual(k.state, KernelState.BOOT)
        k.start()
        self.assertTrue(k.running)

    def test_pause_resume(self):
        k = SimulationKernel()
        k.start()
        k.pause()
        self.assertFalse(k.running)
        k.resume()
        self.assertTrue(k.running)

    def test_fail_transition(self):
        k = SimulationKernel()
        k.start()
        k.fail("test error")
        self.assertEqual(k.state, KernelState.FAILED)


class TestCivilizationRuntime(unittest.TestCase):

    def _make_context(self, **cfg_kwargs):
        bus = EventBus()
        registry = ServiceRegistry()
        telemetry = CognitiveTelemetry()
        telemetry.attach_to_bus(bus)
        config = SimulationConfig(ticks_per_day=2, days_per_epoch=2, **cfg_kwargs)
        return RuntimeContext(bus=bus, registry=registry, clock=None,
                              telemetry=telemetry, config=config)

    def test_world_tick_propagates(self):
        ctx = self._make_context()
        world = World()
        civ = Civilization("Alpha")
        s = Settlement("S1")
        civ.add_settlement(s)
        world.add_civilization(civ)
        world.tick(ctx)  # should not raise

    def test_epoch_event_emitted(self):
        ctx = self._make_context()
        epochs_seen = []
        ctx.bus.subscribe("EPOCH_ADVANCED", lambda e, p: epochs_seen.append(p))
        world = World()
        civ = Civilization("Beta")
        world.add_civilization(civ)
        for _ in range(4):  # ticks_per_epoch = 2*2 = 4
            world.tick(ctx)
        self.assertGreaterEqual(len(epochs_seen), 1)

    def test_total_population(self):
        world = World()
        civ = Civilization("Gamma")
        s = Settlement("G1")
        agent = CognitiveAgent("A1")
        s.add_agent(agent)
        civ.add_settlement(s)
        world.add_civilization(civ)
        self.assertEqual(world.total_population, 1)


class TestSimulationHierarchy(unittest.TestCase):

    def _make_context(self, pipeline=None):
        from runtime.config.simulation_config import DEFAULT_PIPELINE
        bus = EventBus()
        registry = ServiceRegistry()
        telemetry = CognitiveTelemetry()
        telemetry.attach_to_bus(bus)
        config = SimulationConfig(
            ticks_per_day=1, days_per_epoch=1,
            tick_pipeline=pipeline or list(DEFAULT_PIPELINE)
        )
        return RuntimeContext(bus=bus, registry=registry, clock=None,
                              telemetry=telemetry, config=config)

    def test_simulation_runs_without_raising(self):
        from runtime.civilization.simulation import Simulation
        ctx = self._make_context()
        world = World()
        civ = Civilization("Delta")
        world.add_civilization(civ)
        sim = Simulation(world, ctx)
        snapshot = sim.run(cycles=5)
        self.assertIn("buffer_size", snapshot)

    def test_configurable_pipeline_order(self):
        """Simulation with reversed pipeline executes without error."""
        from runtime.civilization.simulation import Simulation
        from runtime.config.simulation_config import DEFAULT_PIPELINE
        reversed_pipeline = list(reversed(DEFAULT_PIPELINE))
        ctx = self._make_context(pipeline=reversed_pipeline)
        self.assertEqual(ctx.config.tick_pipeline[0], "telemetry")
        world = World()
        sim = Simulation(world, ctx)
        snapshot = sim.run(cycles=3)
        self.assertIsNotNone(snapshot)

    def test_global_and_local_systems_separate(self):
        from runtime.civilization.environment import Environment, ClimateSystem, ResourcePoolSystem
        env = Environment()
        global_names = [s.name for s in env.global_systems]
        local_names  = [s.name for s in env.local_systems]
        self.assertIn("Climate", global_names)
        self.assertIn("ResourcePool", local_names)
        # Climate is NOT in local
        self.assertNotIn("Climate", local_names)

    def test_world_owns_environment_not_orchestration(self):
        """World.tick() does not reference SimulationKernel."""
        import inspect
        from runtime.civilization import world as world_module
        source = inspect.getsource(world_module)
        self.assertNotIn("SimulationKernel", source)
        self.assertNotIn("SimulationLoop", source)

    def test_simulation_kernel_hierarchy(self):
        """Simulation wraps Kernel — World does not."""
        from runtime.civilization.simulation import Simulation
        ctx = self._make_context()
        world = World()
        sim = Simulation(world, ctx)
        self.assertIsNotNone(sim.kernel)
        self.assertFalse(hasattr(world, "kernel"))


if __name__ == "__main__":
    unittest.main()
