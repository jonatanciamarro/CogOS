class DecisionEngine:
    """
    DecisionEngine selects action paths based on expected utility metrics.
    """
    @staticmethod
    def evaluate_options(options, utility_function):
        """
        Picks the option with the highest computed score.
        """
        best_option = None
        best_score = -1e9

        for option in options:
            score = utility_function(option)
            if score > best_score:
                best_score = score
                best_option = option

        return best_option
