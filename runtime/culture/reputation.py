class HistoricalReputation:
    """
    HistoricalReputation computes long-term agent credibility ratings based on validated contributions.
    """
    def __init__(self):
        self.proposals_count = {}  # agent_id -> total_proposals
        self.commits_count = {}     # agent_id -> total_commits

    def record_proposal(self, agent_id):
        self.proposals_count[agent_id] = self.proposals_count.get(agent_id, 0) + 1

    def record_commit(self, agent_id):
        self.commits_count[agent_id] = self.commits_count.get(agent_id, 0) + 1

    def get_reputation(self, agent_id):
        """
        Calculates the ratio: validated_commits / total_proposals. Defaults to 0.50.
        """
        proposals = self.proposals_count.get(agent_id, 0)
        if proposals == 0:
            return 0.50
        
        commits = self.commits_count.get(agent_id, 0)
        return commits / proposals
