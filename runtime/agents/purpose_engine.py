from runtime.agents.purpose_history import PurposeHistory

class PurposeEngine:
    """
    PurposeEngine governs proposals, verification, and commits to the CR8 Purpose Vector.
    """
    def __init__(self, agent):
        self.agent = agent
        self.history = PurposeHistory()

    def propose_goal_change(self, new_goal, evidence_uri, omega_cost):
        """
        Processes goal mutation proposals. Rejects if they violate agent constitution rules.
        """
        # 1. Constitution compliance validation
        if not self.agent.constitution.check_goal_compliance(new_goal):
            self.agent.event_log.append("PURPOSE_CHANGE_DENIED", self.agent.identity.agent_id, {"proposed_goal": new_goal})
            raise PermissionError("INT_AGENT_CONSTITUTION: Proposed goal violates Agent Constitution.")

        # 2. Update purpose parameters
        old_goal = self.agent.purpose_vector["goal"]
        self.agent.purpose_vector["goal"] = new_goal

        # 3. Save mutation details to log
        record = self.history.log_mutation(old_goal, new_goal, evidence_uri, omega_cost)
        
        # 4. Append audit event to log
        self.agent.event_log.append("PURPOSE_MUTATED", self.agent.identity.agent_id, record)
        return record
