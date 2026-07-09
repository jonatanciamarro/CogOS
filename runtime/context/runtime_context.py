from dataclasses import dataclass
from runtime.context.service_registry import ServiceRegistry
from runtime.config.simulation_config import SimulationConfig


@dataclass(frozen=True)
class RuntimeContext:
    """
    RuntimeContext is the immutable backbone of CogOS.
    It holds only infrastructure — subsystems are resolved via registry.
    This dataclass NEVER grows: new subsystems go into registry, not here.

    Usage:
        scheduler = ctx.registry.resolve(SchedulerProtocol)
        economy   = ctx.registry.resolve(EconomyProtocol)
    """
    bus:       object            # EventBusProtocol
    registry:  ServiceRegistry
    clock:     object            # CognitiveClock
    telemetry: object            # TelemetryProtocol
    config:    SimulationConfig
