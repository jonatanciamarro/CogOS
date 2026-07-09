class DevelopmentEngine:
    """
    DevelopmentEngine measures agent lifetime cycles, concept node size, and cognitive maturity.
    """
    def __init__(self):
        self.cognitive_age = 0

    def increment_age(self, ticks=1):
        self.cognitive_age += ticks

    def get_developmental_stage(self, node_count):
        """
        Determines developmental category based on ticks and memory size.
        """
        if self.cognitive_age < 100 or node_count < 10:
            return "GENESIS"
        elif self.cognitive_age < 1000 or node_count < 50:
            return "OPERATIONAL"
        return "EVOLVED"
