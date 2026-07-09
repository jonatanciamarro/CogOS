class SelfAssessment:
    """
    SelfAssessment logs action successes and failures to adjust self-confidence in capabilities.
    """
    def __init__(self):
        self.capability_history = {}  # capability_name -> [success_count, failure_count]
        self.capability_confidence = {}  # capability_name -> confidence_score (0.0 to 1.0)

    def record_trial(self, capability_name, success):
        """
        Updates self-confidence scores. Consecutive failures decrease confidence.
        """
        if capability_name not in self.capability_history:
            self.capability_history[capability_name] = [0, 0]
            self.capability_confidence[capability_name] = 0.5

        if success:
            self.capability_history[capability_name][0] += 1
            self.capability_confidence[capability_name] = min(1.0, self.capability_confidence[capability_name] + 0.10)
        else:
            self.capability_history[capability_name][1] += 1
            self.capability_confidence[capability_name] = max(0.0, self.capability_confidence[capability_name] - 0.20)

        return self.capability_confidence[capability_name]
