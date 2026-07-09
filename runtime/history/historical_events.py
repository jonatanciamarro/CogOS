class HistoricalEvent:
    """
    HistoricalEvent structures population censes and milestone events in the timeline.
    """
    def __init__(self, cycle, epoch, event_type, actor_id, details=None):
        self.cycle = cycle
        self.epoch = epoch
        self.type = event_type  # SPAWN, DEPRECATE, DISCOVERY, DISPUTE, MUTATION
        self.actor = actor_id
        self.details = details if details else {}
