class RollbackManager:
    """
    RollbackManager stores delta snapshots (dict diffs) to restore agent state
    without the memory cost of full deepcopies.
    """
    def __init__(self):
        self._snapshots = {}   # agent_id -> list of delta dicts

    def checkpoint(self, agent):
        """
        Records a delta of the agent's current mutable state vs its previous snapshot.
        Only changed attributes are stored.
        """
        agent_id = agent.identity.agent_id
        current = self._extract_state(agent)

        if agent_id not in self._snapshots:
            self._snapshots[agent_id] = [current]
            return

        previous = self._snapshots[agent_id][-1]
        delta = {k: v for k, v in current.items() if previous.get(k) != v}

        if delta:
            self._snapshots[agent_id].append(delta)

    def restore(self, agent):
        """
        Rolls back the agent to its last checkpoint by applying deltas in reverse.
        """
        agent_id = agent.identity.agent_id
        snapshots = self._snapshots.get(agent_id, [])
        if not snapshots:
            return False

        # Reconstruct prior state from base + deltas up to second-to-last
        merged = {}
        for delta in snapshots[:-1]:
            merged.update(delta)

        self._apply_state(agent, merged)
        self._snapshots[agent_id] = snapshots[:-1]
        return True

    def _extract_state(self, agent) -> dict:
        return {
            "lifecycle_state":  agent.lifecycle_state,
            "cognitive_phase":  agent.cognitive_phase,
            "purpose_vector":   dict(agent.purpose_vector),
        }

    def _apply_state(self, agent, state: dict):
        for k, v in state.items():
            setattr(agent, k, v)
