import time
from enum import Enum
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any
from runtime.economy.utility_policy import UtilityEvaluation


class DecisionAction(str, Enum):
    ACCEPT  = "ACCEPT"
    COUNTER = "COUNTER"
    REJECT  = "REJECT"
    DEFER   = "DEFER"


class DecisionFactor(str, Enum):
    """Factors driving agent trade decision scores."""
    UTILITY     = "UTILITY"
    RISK        = "RISK"
    EXPLORATION = "EXPLORATION"


@dataclass(frozen=True)
class DecisionEvaluation:
    """
    Decoupled structure representing the evaluation weights.
    Separates score aggregation from decision execution.
    """
    utility:     UtilityEvaluation
    risk:        float
    exploration: float
    score:       float


@dataclass(frozen=True)
class DecisionResult:
    """
    Result of a DecisionPolicy resolution.
    Fully interpretable, carries latency metric and dominant factor.
    """
    action:           DecisionAction
    evaluation:       DecisionEvaluation
    dominant_factor:  DecisionFactor
    explanation:      str
    decision_latency: float


@runtime_checkable
class DecisionPolicy(Protocol):
    """
    PEP 544 Protocol for pure decision-making evaluators.
    """
    def decide(self, evaluation: DecisionEvaluation) -> DecisionResult:
        ...


class WeightedDecisionPolicy:
    """
    Default pure DecisionPolicy.
    Aggregates utility, risk, and exploration with configurable weights:
    Score = (UtilityDelta * w_util) + (Risk * w_risk) + (Exploration * w_exp)
    """
    def __init__(self, w_util: float = 1.0, w_risk: float = -1.0, w_exp: float = 0.5,
                 accept_threshold: float = 0.0, defer_threshold: float = -0.5):
        self.w_util           = w_util
        self.w_risk           = w_risk
        self.w_exp            = w_exp
        self.accept_threshold = accept_threshold
        self.defer_threshold  = defer_threshold

    def evaluate_decision(self, utility_eval: UtilityEvaluation, risk: float,
                          exploration: float) -> DecisionEvaluation:
        """Helper to create a DecisionEvaluation by applying the linear score formula."""
        score = (utility_eval.delta * self.w_util) + (risk * self.w_risk) + (exploration * self.w_exp)
        return DecisionEvaluation(
            utility=utility_eval,
            risk=risk,
            exploration=exploration,
            score=score
        )

    def decide(self, evaluation: DecisionEvaluation) -> DecisionResult:
        """
        Determines the Action based on the DecisionEvaluation score.
        Must be a pure function: no side-effects.
        """
        t0 = time.perf_counter()

        # Dominant factor detection
        u_val = abs(evaluation.utility.delta * self.w_util)
        r_val = abs(evaluation.risk * self.w_risk)
        e_val = abs(evaluation.exploration * self.w_exp)

        max_val = u_val
        dominant = DecisionFactor.UTILITY

        if r_val > max_val:
            max_val = r_val
            dominant = DecisionFactor.RISK
        if e_val > max_val:
            max_val = e_val
            dominant = DecisionFactor.EXPLORATION

        # Action mapping
        if evaluation.score >= self.accept_threshold:
            action = DecisionAction.ACCEPT
        elif evaluation.score >= self.defer_threshold:
            action = DecisionAction.DEFER
        else:
            action = DecisionAction.REJECT

        latency = time.perf_counter() - t0

        explanation = (
            f"Decision Action: {action.value} (score={evaluation.score:.4f}, "
            f"dominant={dominant.value}, latency={latency * 1000:.3f}ms)"
        )

        return DecisionResult(
            action=action,
            evaluation=evaluation,
            dominant_factor=dominant,
            explanation=explanation,
            decision_latency=latency
        )

