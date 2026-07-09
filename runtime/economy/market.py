class IdeaEntry:
    """
    IdeaEntry tracks investment metadata for a single hypothesis in the IdeaMarket.
    """
    def __init__(self, hypothesis_id):
        self.id = hypothesis_id
        self.resource_invested = 0.0
        self.citation_count    = 0
        self.eig               = 0.5   # Expected Information Gain (0.0–1.0)
        self.risk              = 0.3   # Probability of negative outcome
        self.impact_expected   = 0.5   # Estimated societal impact
        self.idle_epochs       = 0     # Epochs without investment


class IdeaMarket:
    """
    IdeaMarket directs scientific investment using Expected Value of Information (EVI).
    EVI = (EIG × impact_expected) / (cost_estimate × (1 + risk))
    """
    def __init__(self, idle_sweep_threshold: int = 3):
        self.ideas = {}     # hypothesis_id -> IdeaEntry
        self.idle_sweep_threshold = idle_sweep_threshold

    def register_hypothesis(self, hypothesis_id: str) -> IdeaEntry:
        entry = IdeaEntry(hypothesis_id)
        self.ideas[hypothesis_id] = entry
        return entry

    def invest(self, hypothesis_id: str, agent_budget, amount: int) -> bool:
        """
        Agent invests experiment_budget into a hypothesis.
        Returns True if budget was available.
        """
        result = agent_budget.consume("energy", amount)
        if result.ok:
            entry = self.ideas.setdefault(hypothesis_id, IdeaEntry(hypothesis_id))
            entry.resource_invested += amount
            entry.idle_epochs = 0
        return result.ok

    def _evi(self, entry: IdeaEntry) -> float:
        """
        EVI = (EIG × impact_expected) / (resource_invested × (1 + risk))
        """
        cost = max(1.0, entry.resource_invested)
        return (entry.eig * entry.impact_expected) / (cost * (1.0 + entry.risk))

    def rank_by_evi(self) -> list:
        """
        Returns list of (hypothesis_id, evi_score) sorted descending.
        """
        ranked = [(hid, self._evi(e)) for hid, e in self.ideas.items()]
        ranked.sort(key=lambda x: -x[1])
        return ranked

    def tick_idle(self, event_bus=None):
        """
        Increments idle epoch counter; emits SELECTION_SWEEP for neglected hypotheses.
        """
        from runtime.bus.event_bus import CogOSEvents, EventPriority
        for hid, entry in list(self.ideas.items()):
            entry.idle_epochs += 1
            if entry.idle_epochs >= self.idle_sweep_threshold and event_bus:
                event_bus.publish(
                    CogOSEvents.SELECTION_SWEEP,
                    {"hypothesis_id": hid, "reason": "idle"},
                    EventPriority.NORMAL
                )
