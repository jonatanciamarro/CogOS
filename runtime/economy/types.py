from enum import Enum
from dataclasses import dataclass, field
from typing import Any, NewType

# ─── Strongly Typed IDs (wrappers of immutable strings) ─────────────────────────
# Defined as simple type aliases or NewTypes to avoid runtime boilerplate.
AgentId      = NewType("AgentId", str)
ProposalId   = NewType("ProposalId", str)
TradeId      = NewType("TradeId", str)
HypothesisId = NewType("HypothesisId", str)
SettlementId = NewType("SettlementId", str)


# ─── Resource & Knowledge Types ────────────────────────────────────────────────
class ResourceType(str, Enum):
    """Numerical or physical resources tracked in the Agent budgets."""
    ENERGY    = "ENERGY"
    ATTENTION = "ATTENTION"
    CPU       = "CPU"
    MEMORY    = "MEMORY"
    CREDIT    = "CREDIT"


class KnowledgeArtifactType(str, Enum):
    """Qualitative or symbolic scientific artifacts."""
    KNOWLEDGE  = "KNOWLEDGE"
    MEME       = "MEME"
    HYPOTHESIS = "HYPOTHESIS"


@dataclass(frozen=True)
class TradeItem:
    """
    TradeItem is the atomic traded object.
    It is fully immutable. Metadata is a tuple of key-value pairs (tuple of tuples)
    to guarantee hashability and deterministic replayability.
    """
    resource_type: ResourceType | KnowledgeArtifactType
    amount: float
    item_id: str | None = None
    metadata: tuple[tuple[str, Any], ...] = ()


# ─── Trade Negotiation States ──────────────────────────────────────────────────
class TradeStatus(str, Enum):
    """Strictly frozen negotiation states for trade event logging and audit."""
    PROPOSED  = "PROPOSED"
    COUNTER   = "COUNTER"
    ACCEPTED  = "ACCEPTED"
    COMMITTED = "COMMITTED"
    EXECUTED  = "EXECUTED"
    REJECTED  = "REJECTED"
    DEFERRED  = "DEFERRED"
    EXPIRED   = "EXPIRED"
