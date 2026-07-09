class ValueSystem:
    """
    ValueSystem arbitrates target decisions by matching options against value vectors.
    """
    def __init__(self, exploration_weight=0.6, preservation_weight=0.4):
        self.exploration_weight = exploration_weight
        self.preservation_weight = preservation_weight

    def arbitrate(self, options):
        """
        Selects the best goal option matching value utility weights.
        """
        best_option = None
        best_score = -1e9

        for option in options:
            exp_val = option.get("exploration_utility", 0.0)
            pres_val = option.get("preservation_utility", 0.0)
            
            score = (exp_val * self.exploration_weight) + (pres_val * self.preservation_weight)
            if score > best_score:
                best_score = score
                best_option = option

        return best_option
