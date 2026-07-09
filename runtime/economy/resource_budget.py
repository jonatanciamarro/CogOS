from dataclasses import dataclass

@dataclass
class BudgetResult:
    """
    Structured result from a resource consumption attempt.
    Allows callers to react differently per resource type.
    """
    ok: bool
    status: str       # OK | INSUFFICIENT_CPU | INSUFFICIENT_MEMORY | INSUFFICIENT_ATTENTION | INSUFFICIENT_ENERGY
    dimension: str
    deficit: int      # how many units were short (0 if ok)


class ResourceBudget:
    """
    ResourceBudget tracks finite per-tick resource balances for a single agent.
    """
    def __init__(self, policy: dict):
        self.balances = dict(policy)

    def consume(self, dimension: str, amount: int) -> BudgetResult:
        current = self.balances.get(dimension, 0)
        if current >= amount:
            self.balances[dimension] = current - amount
            return BudgetResult(ok=True, status="OK", dimension=dimension, deficit=0)
        deficit = amount - current
        status = f"INSUFFICIENT_{dimension.upper()}"
        return BudgetResult(ok=False, status=status, dimension=dimension, deficit=deficit)

    def replenish(self, dimension: str, amount: int):
        self.balances[dimension] = self.balances.get(dimension, 0) + amount
