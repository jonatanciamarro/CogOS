from dataclasses import dataclass
from typing import Any
from runtime.economy.types import AgentId, ResourceType, KnowledgeArtifactType
from runtime.social.matching_policy import MatchingPolicy, ScarcityPolicy


@dataclass(frozen=True)
class TradeOpportunity:
    """
    Represents a potential barter opportunity discovered between two agents.
    Does not modify any state; acts as input to the DecisionPolicy.
    """
    from_agent_id:    AgentId
    to_agent_id:      AgentId
    offered_resource: ResourceType | KnowledgeArtifactType
    requested_resource: ResourceType | KnowledgeArtifactType


class MatchingEngine:
    """
    MatchingEngine queries active agents and finds TradeOpportunities
    using an injected MatchingPolicy strategy.
    """
    def __init__(self, policy: MatchingPolicy = None):
        self.policy = policy or ScarcityPolicy()

    def find_opportunities(self, agents_by_id: dict[AgentId, Any], ctx: Any) -> list[TradeOpportunity]:
        """
        Delegates the matching strategy to the injected policy.
        """
        return self.policy.find_matches(agents_by_id, ctx)
