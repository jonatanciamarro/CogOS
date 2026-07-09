import random


# ─── Global Systems (affect all civilizations) ────────────────────────────────

class GlobalResourceFlowSystem:
    """
    GlobalSystem: models shared resource flow across all civilizations.
    A drought here affects every Settlement's energy pool.
    """
    name = "GlobalResourceFlow"

    def __init__(self, base_flow: int = 10):
        self.base_flow = base_flow
        self.current_flow = base_flow

    def tick(self, context) -> None:
        variance = random.uniform(-0.2, 0.2)
        self.current_flow = max(0, int(self.base_flow * (1 + variance)))


class ClimateSystem:
    """
    GlobalSystem: generates climate events that all civilizations observe.
    """
    name = "Climate"

    EVENTS = ["drought", "flood", "ideal", "storm", "cold_snap"]

    def __init__(self, event_prob: float = 0.08):
        self.event_prob = event_prob
        self.current_climate = "ideal"

    def tick(self, context) -> None:
        if random.random() < self.event_prob:
            self.current_climate = random.choice(self.EVENTS)
            bus = getattr(context, "bus", None)
            if bus:
                from runtime.bus.event_bus import EventPriority
                bus.publish("CLIMATE_EVENT",
                            {"type": self.current_climate},
                            EventPriority.HIGH)
        else:
            self.current_climate = "ideal"


# ─── Local Systems (affect a single Settlement) ────────────────────────────────

class ResourcePoolSystem:
    """
    LocalSystem: manages local energy resource pool per Settlement.
    """
    name = "ResourcePool"

    def __init__(self, initial_energy: int = 1000, regeneration_rate: int = 10):
        self.energy = initial_energy
        self.regeneration_rate = regeneration_rate

    def tick(self, context) -> None:
        self.energy = min(10000, self.energy + self.regeneration_rate)

    def consume(self, amount: int) -> bool:
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False


class RandomEventSystem:
    """
    LocalSystem: stochastic local events (disease, collapse, windfall).
    Only the Settlement that owns this system is affected.
    """
    name = "RandomEvents"

    def __init__(self, scarcity_prob: float = 0.05, abundance_prob: float = 0.03,
                 catastrophe_prob: float = 0.01):
        self.scarcity_prob    = scarcity_prob
        self.abundance_prob   = abundance_prob
        self.catastrophe_prob = catastrophe_prob

    def tick(self, context) -> None:
        from runtime.bus.event_bus import EventPriority
        bus = getattr(context, "bus", None)
        if bus is None:
            return
        r = random.random()
        if r < self.catastrophe_prob:
            bus.publish("ENV_CATASTROPHE", {"severity": "high", "scope": "local"},
                        EventPriority.CRITICAL)
        elif r < self.catastrophe_prob + self.scarcity_prob:
            bus.publish("ENV_SCARCITY", {"resource": "energy", "scope": "local"},
                        EventPriority.HIGH)
        elif r < self.catastrophe_prob + self.scarcity_prob + self.abundance_prob:
            bus.publish("ENV_ABUNDANCE", {"resource": "energy", "scope": "local"},
                        EventPriority.NORMAL)


# ─── Environment ──────────────────────────────────────────────────────────────

class Environment:
    """
    Environment separates global (cross-civilization) systems from local (per-settlement) ones.

    GlobalSystems:  Climate, Astronomy, GlobalResourceFlow — affect every Civilization.
    LocalSystems:   ResourcePool, LocalEcology, Infrastructure — affect one Settlement.

    Sprint 5.4 adds TechnologySystem (local) and AstronomySystem (global) without touching this class.
    """
    def __init__(self, global_systems: list = None, local_systems: list = None):
        self.global_systems = global_systems or [
            GlobalResourceFlowSystem(),
            ClimateSystem(),
        ]
        self.local_systems = local_systems or [
            ResourcePoolSystem(),
            RandomEventSystem(),
        ]

    def tick_global(self, context) -> None:
        """Tick all global systems — called once per World tick."""
        for system in self.global_systems:
            system.tick(context)

    def tick_local(self, context) -> None:
        """Tick all local systems — called once per Settlement tick."""
        for system in self.local_systems:
            system.tick(context)

    def tick(self, context) -> None:
        """Convenience: tick both layers (used when not separately orchestrated)."""
        self.tick_global(context)
        self.tick_local(context)

    def get_system(self, name: str):
        all_systems = self.global_systems + self.local_systems
        return next((s for s in all_systems if s.name == name), None)
