class WorldModelEngine:
    """
    WorldModelEngine simulates hypothetical action outcomes and forecasts future environment states.
    """
    def __init__(self):
        # Maps (state_condition, action) -> predicted_outcome_state
        self.causal_rules = {}

    def register_rule(self, state_condition, action, predicted_outcome):
        self.causal_rules[(state_condition, action)] = predicted_outcome

    def simulate(self, current_state, action):
        """
        Forecasts the expected outcome of an action in the current state context.
        """
        return self.causal_rules.get((current_state, action), current_state)
