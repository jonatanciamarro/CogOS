class Epoch:
    """
    Epoch packages a sequence of historical events and civilization metrics.
    """
    def __init__(self, epoch_number):
        self.number = epoch_number
        self.events = []
        self.metrics_summary = {}

    def log_event(self, event):
        self.events.append(event)

    def set_metrics(self, key, value):
        self.metrics_summary[key] = value
