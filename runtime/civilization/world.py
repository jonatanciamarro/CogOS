from runtime.civilization.environment import Environment
from runtime.world.evolution_state import EvolutionaryPressure


class World:
    """
    World represents the shared space that all Civilizations inhabit.
    Responsibilities: global environment tick, inter-civilization events.
    Orchestration (loop, kernel, phases) belongs to Simulation — not here.
    Sprint 5.X adds a second Civilization here without touching any other module.
    """
    def __init__(self, name: str = "CogOS World", environment: Environment = None):
        self.name = name
        self.civilizations: list = []
        self.environment = environment or Environment()
        self.evolution_pressure = EvolutionaryPressure()

    def add_civilization(self, civilization) -> None:
        self.civilizations.append(civilization)

    def tick(self, context) -> None:
        # Tick evolutionary pressure decay
        self.evolution_pressure.decay()

        # Global environment affects every civilization
        self.environment.tick_global(context)

        for civilization in self.civilizations:
            civilization.tick(context)

    @property
    def total_population(self) -> int:
        return sum(c.total_population for c in self.civilizations)
