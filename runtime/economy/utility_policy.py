from enum import Enum
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any
from runtime.economy.utility_context import UtilityContext
from runtime.economy.utility_function import UtilityFunction, WeightedLogUtilityFunction
from runtime.economy.types import ResourceType, KnowledgeArtifactType


class UtilityComponent(str, Enum):
    """
    Categorized utility components representing the dimensions of agent utility.
    """
    ENERGY    = "ENERGY"
    KNOWLEDGE = "KNOWLEDGE"
    TRUST     = "TRUST"
    NOVELTY   = "NOVELTY"
    ATTENTION = "ATTENTION"


@dataclass(frozen=True)
class UtilityEvaluation:
    """
    Immutable evaluation of a state transition delta.
    Provides complete explanation and breakdown per component.
    """
    before:      float
    after:       float
    delta:       float
    confidence:  float
    explanation: str | None
    components:  dict[UtilityComponent, float]


@runtime_checkable
class UtilityPolicy(Protocol):
    """
    PEP 544 Protocol for comparing absolute utility state transitions.
    Must be a pure function: no side-effects.
    """
    def delta(self, before: Any, after: Any, ctx: UtilityContext) -> UtilityEvaluation:
        ...


class DeltaUtilityPolicy:
    """
    Default UtilityPolicy implementing state comparison via an injected UtilityFunction.
    """
    def __init__(self, utility_function: UtilityFunction = None):
        self.utility_func = utility_function or WeightedLogUtilityFunction()

    def delta(self, before: Any, after: Any, ctx: UtilityContext) -> UtilityEvaluation:
        """
        Computes the delta utility between before and after states.
        Breaks down the delta contribution per component.
        """
        before_val = self.utility_func.evaluate(before, ctx)
        after_val  = self.utility_func.evaluate(after, ctx)
        diff       = after_val - before_val

        # Compute component breakdown (safe extraction)
        components = {}
        if isinstance(self.utility_func, WeightedLogUtilityFunction):
            import math
            # Calculate all budget resource deltas
            for res_name, weight in self.utility_func.weights.items():
                b_val = self._read_res(before, res_name)
                a_val = self._read_res(after, res_name)
                d_res = weight * (math.log1p(max(0.0, float(a_val))) - math.log1p(max(0.0, float(b_val))))
                
                try:
                    component = UtilityComponent(res_name.upper())
                    components[component] = d_res
                except ValueError:
                    pass

            b_know  = self._read_knowledge(before)
            b_trust = getattr(before, "trust_score", 0.5)

            a_know  = self._read_knowledge(after)
            a_trust = getattr(after, "trust_score", 0.5)

            d_know   = self.utility_func.w_knowledge * (math.sqrt(max(0.0, float(a_know))) - math.sqrt(max(0.0, float(b_know))))
            d_trust  = self.utility_func.w_trust * (float(a_trust) - float(b_trust))

            components[UtilityComponent.KNOWLEDGE] = d_know
            components[UtilityComponent.TRUST]     = d_trust

        explanation = f"Utility state transitioned from {before_val:.4f} to {after_val:.4f} (delta={diff:.4f})"

        return UtilityEvaluation(
            before=before_val,
            after=after_val,
            delta=diff,
            confidence=1.0,
            explanation=explanation,
            components=components
        )

    def _read_res(self, state, resource_name: str) -> float:
        if hasattr(state, "resource_budget") and state.resource_budget:
            return state.resource_budget.balances.get(resource_name.lower(), 0.0)
        elif hasattr(state, "resource_amount"):
            # Simple conversion string to ResourceType
            try:
                r_type = ResourceType(resource_name.upper())
                return state.resource_amount(r_type)
            except ValueError:
                pass
        return getattr(state, resource_name.lower(), 0.0)

    def _read_knowledge(self, state) -> float:
        if hasattr(state, "resource_amount"):
            return state.resource_amount(KnowledgeArtifactType.KNOWLEDGE)
        return getattr(state, "knowledge", 0.0)
