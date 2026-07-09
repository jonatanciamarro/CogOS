class StrategyMemory:
    """
    StrategyMemory stores plans, goal sequences, and heuristic heuristics of the agent.
    """
    def __init__(self):
        self.logs = []

    def add_strategy(self, description):
        self.logs.append(description)
