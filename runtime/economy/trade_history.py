from dataclasses import dataclass
from runtime.economy.types import ProposalId
from runtime.social.trade_proposal import TradeProposal


@dataclass(frozen=True)
class TradeHistoryEvent:
    """
    An immutable event logged into the trade ledger.
    """
    event_type: str  # e.g., 'ProposalCreated', 'CounterCreated', 'Accepted', 'Committed', 'Executed'
    proposal:   TradeProposal
    timestamp:  float


class TradeHistory:
    """
    Event-Sourced, append-only log of economic trade negotiations.
    Never mutates or deletes records in-place.
    """
    def __init__(self):
        self._events: list[TradeHistoryEvent] = []

    def append(self, event_type: str, proposal: TradeProposal, timestamp: float) -> None:
        """Appends a new event to the ledger."""
        self._events.append(
            TradeHistoryEvent(event_type=event_type, proposal=proposal, timestamp=timestamp)
        )

    def get_events(self) -> list[TradeHistoryEvent]:
        """Returns a copy of the events list."""
        return list(self._events)

    def reconstruct_proposal(self, proposal_id: ProposalId) -> TradeProposal | None:
        """
        Reconstructs the proposal state by replaying events up to the latest status.
        """
        latest = None
        for event in self._events:
            if event.proposal.proposal_id == proposal_id:
                latest = event.proposal
        return latest

    def get_chain(self, leaf_proposal_id: ProposalId) -> list[TradeProposal]:
        """
        Reconstructs the negotiation history chain (P0 -> P1 -> P2).
        Returns proposals in chronological order.
        """
        proposals_by_id = {event.proposal.proposal_id: event.proposal for event in self._events}
        
        chain = []
        current_id = leaf_proposal_id
        while current_id is not None:
            prop = proposals_by_id.get(current_id)
            if not prop:
                break
            chain.insert(0, prop)  # prepend to keep chronological order
            current_id = prop.parent_id
        return chain
