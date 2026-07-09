class Coalition:
    """
    Coalition defines a group of agents cooperating on a shared goal task.
    """
    def __init__(self, coalition_id, shared_goal):
        self.id = coalition_id
        self.shared_goal = shared_goal
        self.members = []

    def join(self, agent_id):
        if agent_id not in self.members:
            self.members.append(agent_id)


class CoalitionEngine:
    """
    CoalitionEngine dynamically manages, spawns, and terminates agent coalitions.
    """
    def __init__(self):
        self.coalitions = {}

    def form_coalition(self, coalition_id, shared_goal, agent_ids):
        """
        Gathers member agents under a unique coalition ID.
        """
        coalition = Coalition(coalition_id, shared_goal)
        for agent_id in agent_ids:
            coalition.join(agent_id)
        self.coalitions[coalition_id] = coalition
        return coalition

    def dissolve_coalition(self, coalition_id):
        self.coalitions.pop(coalition_id, None)
