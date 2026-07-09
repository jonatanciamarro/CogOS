class ConflictProtocol:
    """
    ConflictProtocol resolves disputes and registers local contradiction relations between beliefs.
    """
    @staticmethod
    def register_disagreement(agent, opponent_id, belief_a, belief_b):
        """
        Creates a contradiction edge between the disputed concepts instead of raising interrupts.
        """
        agent.event_log.append("PERSISTENT_DISAGREEMENT", agent.identity.agent_id, {
            "opponent": opponent_id,
            "local_belief": belief_a,
            "opponent_belief": belief_b
        })

        # Returns a structured relation edge
        return {
            "source": belief_a,
            "target": belief_b,
            "relation": "CONTRADICTION",
            "weight": 1.00
        }
