class FailuresMemory:
    """
    FailuresMemory keeps track of rejected hypotheses and failed experiments.
    """
    def __init__(self):
        self.logs = []

    def record_failure(self, hypothesis_uri, anomaly_details):
        self.logs.append({
            "hypothesis": hypothesis_uri,
            "anomaly": anomaly_details
        })
