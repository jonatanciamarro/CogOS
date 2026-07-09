class Hypothesis:
    """
    Hypothesis represents a tentative belief statement waiting for confirmation.
    """
    def __init__(self, hypothesis_id, statement, confidence=0.5):
        self.id = hypothesis_id
        self.statement = statement
        self.confidence = confidence
        self.predictions = []
        self.evidence = []
        self.contradictions = []
        self.status = "ACTIVE"  # ACTIVE, CONFIRMED, REFUTED, EVOLVED


class HypothesisEngine:
    """
    HypothesisEngine creates, modifies, and validates Hypothesis objects based on experiments.
    """
    def __init__(self):
        self.hypotheses = {}

    def generate_hypothesis(self, hypothesis_id, statement):
        hyp = Hypothesis(hypothesis_id, statement)
        self.hypotheses[hypothesis_id] = hyp
        return hyp

    def record_prediction(self, hypothesis_id, prediction):
        hyp = self.hypotheses.get(hypothesis_id)
        if hyp:
            hyp.predictions.append(prediction)

    def evaluate_status(self, hypothesis_id, prediction_correct):
        """
        Updates the hypothesis confidence based on prediction outcomes.
        """
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            return None

        if prediction_correct:
            # Increase confidence
            hyp.confidence = min(1.0, hyp.confidence + 0.15)
            hyp.evidence.append("obs_match")
            if hyp.confidence >= 0.8:
                hyp.status = "CONFIRMED"
        else:
            # Decrease confidence
            hyp.confidence = max(0.0, hyp.confidence - 0.25)
            hyp.contradictions.append("obs_mismatch")
            if hyp.confidence <= 0.2:
                hyp.status = "REFUTED"

        return hyp.status
