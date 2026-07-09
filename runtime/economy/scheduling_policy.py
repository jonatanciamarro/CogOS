from typing import Protocol

class SchedulingPolicy(Protocol):
    """
    PEP 544 Protocol for pluggable task scoring strategies.
    Sprint 5.0 can swap policies without modifying the Executor.
    """
    def score(self, task, agent) -> float:
        ...


class GreedyPolicy:
    """
    Default policy: maximizes utility per cost unit.
    score = (urgency × EIG × efficiency × trust) / estimated_cost
    """
    def score(self, task, agent) -> float:
        urgency    = getattr(task, "urgency", 1.0)
        eig        = getattr(task, "expected_information_gain", 1.0)
        efficiency = getattr(agent, "historical_efficiency", 1.0)
        trust      = getattr(agent, "trust_score", 0.5)
        cost       = max(1.0, getattr(task, "cost_estimate", 1.0))
        return (urgency * eig * efficiency * trust) / cost


class ScientificPolicy:
    """Favours high-EIG tasks regardless of cost — for research-oriented societies."""
    def score(self, task, agent) -> float:
        eig  = getattr(task, "expected_information_gain", 1.0)
        cost = max(1.0, getattr(task, "cost_estimate", 1.0))
        return eig / cost


class EnergySavingPolicy:
    """Favours low-cost tasks — for energy-constrained epochs."""
    def score(self, task, agent) -> float:
        cost = max(1.0, getattr(task, "cost_estimate", 1.0))
        return 1.0 / cost
