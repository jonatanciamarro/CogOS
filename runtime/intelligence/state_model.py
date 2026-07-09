class InternalBelief:
    """
    InternalBelief represents the agent's internal assessment of concepts, confidence, and source evidence.
    """
    def __init__(self, concept, confidence=1.0, uncertainty=0.0):
        self.concept = concept
        self.confidence = confidence
        self.uncertainty = uncertainty
        self.evidence = []

    def update_confidence(self, score):
        self.confidence = max(0.0, min(1.0, score))
        self.uncertainty = 1.0 - self.confidence
