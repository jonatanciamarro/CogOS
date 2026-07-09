from dataclasses import dataclass
from runtime.economy.types import AgentId, ProposalId, TradeItem, TradeStatus


@dataclass(frozen=True)
class TradeProposal:
    """
    TradeProposal is a fully immutable representation of a trade offer or counter-offer.
    
    Rule: Never modify state in-place. Negotiation transitions create a new
    TradeProposal instance linking back to its parent_id, forming a complete audit chain.
    """
    proposal_id:  ProposalId
    parent_id:    ProposalId | None
    from_agent:   AgentId
    to_agent:     AgentId
    offer:        tuple[TradeItem, ...]
    request:      tuple[TradeItem, ...]
    round:        int
    expires_tick: int
    status:       TradeStatus
