from runtime.bus.event_bus import CogOSEvents

# Default credit rewards per event type
DEFAULT_CREDIT_REWARDS = {
    CogOSEvents.PUBLICATION_ACCEPTED: {"scientific_credits": 20},
    CogOSEvents.PEER_REVIEW_PASSED:   {"trust_credits": 10},
    CogOSEvents.EXPERIMENT_COMPLETED: {"innovation_credits": 5},
    CogOSEvents.MEME_PROPAGATED:      {"scientific_credits": 2},
}

# Credit → CPU conversion at epoch boundary (credits spent, cpu replenished)
DEFAULT_CONVERSION_POLICY = {
    "scientific_credits": {"cpu": 50},
    "trust_credits":       {"attention": 5},
    "innovation_credits":  {"energy": 10},
    "publication_credits": {"memory": 20},
}


class CreditLedger:
    """
    CreditLedger manages persistent agent credits earned via EventBus events.
    Credits are decoupled from resource budgets — they convert via policy at epoch boundary.
    """
    def __init__(self):
        self.balances = {
            "scientific_credits": 0,
            "trust_credits":      0,
            "innovation_credits": 0,
            "publication_credits": 0,
        }

    def award(self, event_type: str, rewards: dict = None):
        """
        Awards credits for a given event type using reward mapping.
        """
        source = rewards or DEFAULT_CREDIT_REWARDS.get(event_type, {})
        for credit_type, amount in source.items():
            self.balances[credit_type] = self.balances.get(credit_type, 0) + amount

    def convert_to_resources(self, resource_budget, policy: dict = None):
        """
        At epoch boundary: spend credits, replenish resource budget dimensions.
        """
        conversion = policy or DEFAULT_CONVERSION_POLICY
        for credit_type, resource_map in conversion.items():
            available = self.balances.get(credit_type, 0)
            if available > 0:
                for resource_dim, rate in resource_map.items():
                    units = (available // 10) * rate   # spend 10 credits → rate units
                    if units > 0:
                        resource_budget.replenish(resource_dim, units)
                        self.balances[credit_type] = max(0, available - (units // rate) * 10)
