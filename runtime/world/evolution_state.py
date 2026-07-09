from dataclasses import dataclass

@dataclass
class EvolutionaryPressure:
    environmental_stress: float = 0.1
    scientific_pressure: float = 0.1
    resource_pressure: float = 0.1

    def decay(self) -> None:
        """
        Linear/exponential decay of transient event stress levels back to baseline.
        """
        self.environmental_stress = max(0.1, self.environmental_stress * 0.95)
        self.scientific_pressure = max(0.1, self.scientific_pressure * 0.95)
        self.resource_pressure = max(0.1, self.resource_pressure * 0.95)
