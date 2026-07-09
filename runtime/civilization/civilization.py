from runtime.civilization.environment import Environment
from runtime.bus.event_bus import CogOSEvents, EventPriority


class Civilization:
    """
    Civilization is the intermediate container between World and Settlement.
    It does not know about other Civilizations — that is World's responsibility.
    """
    def __init__(self, name: str, environment: Environment = None):
        self.name = name
        self.settlements: list = []
        self.environment = environment or Environment()
        self._tick = 0

    def add_settlement(self, settlement) -> None:
        self.settlements.append(settlement)

    def tick(self, context) -> None:
        self._tick += 1
        self.environment.tick(context)

        for settlement in self.settlements:
            settlement.tick(context)

        # Emit epoch boundary event when configured ticks elapse
        config = getattr(context, "config", None)
        ticks_per_epoch = getattr(config, "ticks_per_epoch", 50)
        if self._tick % ticks_per_epoch == 0:
            bus = getattr(context, "bus", None)
            if bus:
                bus.publish(CogOSEvents.EPOCH_ADVANCED,
                            {"civilization": self.name, "epoch": self._tick // ticks_per_epoch},
                            EventPriority.HIGH)

    @property
    def total_population(self) -> int:
        return sum(s.population_size for s in self.settlements)
