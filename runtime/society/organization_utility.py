import math
from runtime.society.organization import OrganizationSnapshot


class OrganizationUtilityFunction:
    """
    Evaluates join / leave opportunities of an agent against a laboratory.
    Formula:
    JoinScore = (Uc - Us) - Cc - autonomy_loss
    
    Prevents the "mega-institution" trap by scaling Coordination Cost (Cc) linearly
    with member counts, and dividing collective pooling utility (Uc) amongst shares.
    """
    def __init__(self, coordination_weight: float = 0.05, autonomy_loss: float = 0.15):
        self.coordination_weight = coordination_weight
        self.autonomy_loss        = autonomy_loss

    def evaluate_join_score(self, agent, org: OrganizationSnapshot, solo_utility: float, current_tick: int = 0, ecology_model = None) -> float:
        """
        Computes a float score indicating preference. Positive means join/remain.
        """
        members_count = len(org.members) + 1  # count if the agent joins

        # 1. Uc - Collective Utility: Log resource pool scaled by capacity, split amongst members
        pool_util = 0.0
        for res_name, val in org.resources.balances.items():
            pool_util += math.log1p(max(0.0, float(val)))

        u_collective = (pool_util * org.research_capacity) / float(members_count)

        # 2. Cc - Coordination Cost: Hybrid non-linear formula
        # a * N^1.5 + b * log(N + 1)
        n = float(len(org.members))
        c_coordination = (self.coordination_weight * (n ** 1.5)) + (0.05 * math.log1p(n))

        # 3. Autonomy Loss: Logarithmic scaling based on member counts
        eff_autonomy_loss = self.autonomy_loss * math.log2(n + 2.0)

        # 4. Cooldown Penalty from Ecology Model
        penalty = 0.0
        if ecology_model is not None:
            # Fallback handling for string/object AgentId representation
            agent_id = getattr(agent, "identity", agent)
            agent_id = getattr(agent_id, "agent_id", agent_id)
            penalty = ecology_model.get_cooldown_penalty(agent_id, current_tick)

        # 5. Final score
        score = (u_collective - solo_utility) - c_coordination - eff_autonomy_loss - penalty
        return score
