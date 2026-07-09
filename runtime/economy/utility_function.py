import math
from typing import Protocol, runtime_checkable, Any
from runtime.economy.types import ResourceType, KnowledgeArtifactType
from runtime.economy.utility_context import UtilityContext


@runtime_checkable
class UtilityFunction(Protocol):
    """
    PEP 544 Protocol for absolute state utility evaluation.
    Must be a pure function: no side-effects, fully deterministic.
    """
    def evaluate(self, state: Any, ctx: UtilityContext) -> float:
        ...


class WeightedLogUtilityFunction:
    """
    Default UtilityFunction implementation.
    Evaluates absolute state value using weighted non-linear utility curves:
    - Logarithmic utility for physical resources (diminishing returns)
    - Square root utility for knowledge artifacts
    - Linear utility for trust scores
    """
    def __init__(self, weights: dict[str, float] = None, w_knowledge: float = 1.0, w_trust: float = 1.0, w_energy: float = None):
        self.weights = weights or {"energy": 1.0, "attention": 1.0}
        if w_energy is not None:
            self.weights["energy"] = w_energy
        self.w_knowledge = w_knowledge
        self.w_trust     = w_trust


    @property
    def w_energy(self) -> float:
        """Legacy compatibility helper."""
        return self.weights.get("energy", 1.0)

    def evaluate(self, state: Any, ctx: UtilityContext) -> float:
        """
        Evaluates the absolute utility value of the given state.
        Fuses logarithmic budget resource evaluations with root knowledge evaluations.
        """
        total_utility = 0.0

        # Evaluate budget resources logarithmically (diminishing returns)
        if hasattr(state, "resource_budget") and state.resource_budget:
            for res_name, weight in self.weights.items():
                val = float(state.resource_budget.balances.get(res_name, 0.0))
                total_utility += weight * math.log1p(max(0.0, val))
        else:
            # Safe attribute fallback (legacy)
            energy = getattr(state, "energy", 0.0)
            if hasattr(state, "resource_amount"):
                energy = state.resource_amount(ResourceType.ENERGY)
            total_utility += self.w_energy * math.log1p(max(0.0, float(energy)))

        # Read knowledge
        knowledge = 0.0
        if hasattr(state, "resource_amount"):
            knowledge = state.resource_amount(KnowledgeArtifactType.KNOWLEDGE)
        else:
            knowledge = getattr(state, "knowledge", 0.0)

        # Read trust
        trust = getattr(state, "trust_score", 0.5)

        total_utility += self.w_knowledge * math.sqrt(max(0.0, float(knowledge)))
        total_utility += self.w_trust * float(trust)

        return total_utility

