class ConsensusEngine:
    """
    ConsensusEngine computes weighted consensus scores based on agent reputations and claim evidence.
    """
    @staticmethod
    def evaluate_proposal(votes, reputations):
        """
        votes: list of dicts -> {"agent_id": id, "agree": bool, "confidence": float, "lineage_size": int}
        reputations: dict -> agent_id -> reputation_score (0.0 to 1.0)
        """
        weighted_agreements = 0.0
        weighted_disagreements = 0.0

        for vote in votes:
            agent_id = vote["agent_id"]
            rep = reputations.get(agent_id, 0.50)
            
            # Lineage footprint bonus factor
            lineage_bonus = 1.00 + (0.10 * vote.get("lineage_size", 0))
            vote_weight = vote["confidence"] * rep * lineage_bonus

            if vote["agree"]:
                weighted_agreements += vote_weight
            else:
                weighted_disagreements += vote_weight

        total_weight = weighted_agreements + weighted_disagreements
        if total_weight == 0.0:
            return 0.0

        # Returns consensus ratio between 0.0 and 1.0
        return weighted_agreements / total_weight
