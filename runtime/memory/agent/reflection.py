class ReflectionMemory:
    """
    ReflectionMemory stores core insights, corrections, and strategy adjustments.
    """
    def __init__(self):
        self.logs = []

    def record_insight(self, description):
        self.logs.append(description)
