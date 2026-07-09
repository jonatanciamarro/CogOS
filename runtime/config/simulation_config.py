from dataclasses import dataclass, field
from typing import List


# Default tick pipeline phase order — configurable per simulation
DEFAULT_PIPELINE: List[str] = [
    "observe",
    "plan",
    "allocate_resources",
    "execute",
    "communicate",
    "learn",
    "science",
    "culture",
    "governance",
    "environment_update",
    "history",
    "telemetry",
]


@dataclass
class SimulationConfig:
    """
    SimulationConfig centralizes every constant in CogOS.
    Pass --seed to make any simulation fully reproducible.
    tick_pipeline controls phase order — experiments can reorder phases freely.
    """
    # Time granularity
    ticks_per_day:   int   = 10
    days_per_epoch:  int   = 5

    # Resource economy
    energy_regeneration:  int   = 5
    memory_regeneration:  int   = 20
    idle_sweep_threshold: int   = 3

    # Agent lifecycle
    spawn_probability: float = 0.1

    # IdeaMarket
    market_evi_decay:  float = 0.05

    # Tick pipeline — order is explicit and reproducible
    tick_pipeline: List[str] = field(default_factory=lambda: list(DEFAULT_PIPELINE))

    # Simulation control
    seed:  int  = 42
    debug: bool = False

    @property
    def ticks_per_epoch(self) -> int:
        return self.ticks_per_day * self.days_per_epoch
