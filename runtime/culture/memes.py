class CognitiveMeme:
    """
    CognitiveMeme represents a replicable conceptual idea propagating through the society.
    """
    def __init__(self, meme_id, name, origin_agent_id, confidence=0.5):
        self.id = meme_id
        self.name = name
        self.origin_agent = origin_agent_id
        self.confidence = confidence
        self.adoption_count = 1

    def increment_adoption(self):
        self.adoption_count += 1
        return self.adoption_count
