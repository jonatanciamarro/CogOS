class LearningEngine:
    """
    LearningEngine implements delta weight adjustments and forgetting decay.
    """
    def __init__(self, learning_rate=0.1, forgetting_rate=0.02):
        self.learning_rate = learning_rate
        self.forgetting_rate = forgetting_rate

    def compute_delta_update(self, current_weight, prediction_error):
        """
        Updates weights using delta rules.
        """
        adjustment = self.learning_rate * prediction_error
        updated_weight = current_weight + adjustment
        return max(0.0, min(1.0, updated_weight))

    def decay_weight(self, current_weight):
        """
        Applies exponential/constant decay to obsolete or unvisited weights.
        """
        decayed = current_weight - self.forgetting_rate
        return max(0.0, decayed)
