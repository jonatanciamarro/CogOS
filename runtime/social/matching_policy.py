from typing import Protocol, runtime_checkable, Any
from runtime.economy.types import AgentId, ResourceType


@runtime_checkable
class MatchingPolicy(Protocol):
    """
    PEP 544 Protocol for trade matching algorithms.
    Decoupled from MatchingEngine.
    """
    def find_matches(self, agents_by_id: dict[AgentId, Any], ctx: Any) -> list:
        ...


class ScarcityPolicy:
    """
    Pairs agents with complementary resource levels.
    """
    def find_matches(self, agents_by_id: dict[AgentId, Any], ctx: Any) -> list:
        from runtime.social.matching_engine import TradeOpportunity

        matches = []
        agents = list(agents_by_id.values())

        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                a1 = agents[i]
                a2 = agents[j]

                a1_energy = self._get_res(a1, ResourceType.ENERGY)
                a1_att    = self._get_res(a1, ResourceType.ATTENTION)
                a2_energy = self._get_res(a2, ResourceType.ENERGY)
                a2_att    = self._get_res(a2, ResourceType.ATTENTION)

                # Pair agent having excess energy but low attention with partner who has inverse
                if a1_energy > 500 and a2_energy < 200 and a2_att > 30 and a1_att < 15:
                    matches.append(TradeOpportunity(
                        from_agent_id=a1.identity.agent_id,
                        to_agent_id=a2.identity.agent_id,
                        offered_resource=ResourceType.ENERGY,
                        requested_resource=ResourceType.ATTENTION
                    ))
                elif a2_energy > 500 and a1_energy < 200 and a1_att > 30 and a2_att < 15:
                    matches.append(TradeOpportunity(
                        from_agent_id=a2.identity.agent_id,
                        to_agent_id=a1.identity.agent_id,
                        offered_resource=ResourceType.ENERGY,
                        requested_resource=ResourceType.ATTENTION
                    ))
        return matches

    def _get_res(self, agent, resource_type: ResourceType) -> float:
        budget = getattr(agent, "resource_budget", None)
        if budget:
            return float(budget.balances.get(resource_type.value.lower(), 0.0))
        return 0.0


class RandomMatchingPolicy:
    """
    Simple fallback policy to find matches randomly for testing.
    """
    def find_matches(self, agents_by_id: dict[AgentId, Any], ctx: Any) -> list:
        from runtime.social.matching_engine import TradeOpportunity
        from runtime.economy.types import ResourceType

        matches = []
        agents = list(agents_by_id.values())
        if len(agents) >= 2:
            matches.append(TradeOpportunity(
                from_agent_id=agents[0].identity.agent_id,
                to_agent_id=agents[1].identity.agent_id,
                offered_resource=ResourceType.ENERGY,
                requested_resource=ResourceType.ATTENTION
            ))
        return matches
