class AgentTrustNetwork:
    """
    AgentTrustNetwork tracks and adjusts relative trust scores of neighboring agents.
    """
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.trust_ratings = {}  # agent_id -> trust_score (0.0 to 1.0)

    def get_trust_rating(self, agent_id):
        """
        Returns the trust score of the agent. Defaults to 0.50 if unrated.
        """
        return self.trust_ratings.get(agent_id, 0.50)

    def update_trust(self, agent_id, reward):
        """
        Increases or decreases trust based on transaction success or truth values.
        """
        current = self.get_trust_rating(agent_id)
        if reward:
            self.trust_ratings[agent_id] = min(1.0, current + 0.05)
        else:
            self.trust_ratings[agent_id] = max(0.0, current - 0.15)
        return self.trust_ratings[agent_id]
