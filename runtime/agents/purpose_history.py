import time

class PurposeHistory:
    """
    PurposeHistory tracks the immutable evolution log of an agent's CR8 Purpose Vector.
    """
    def __init__(self):
        self.mutations = []

    def log_mutation(self, old_goal, new_goal, evidence_uri, omega_cost):
        """
        Appends a mutation transaction mapping transition cause and cost metrics.
        """
        record = {
            "timestamp": time.time(),
            "old_goal": old_goal,
            "new_goal": new_goal,
            "evidence": evidence_uri,
            "omega_cost": omega_cost
        }
        self.mutations.append(record)
        return record
