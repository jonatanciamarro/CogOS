from runtime.history.epoch import Epoch
from runtime.history.historical_events import HistoricalEvent

class CivilizationMemory:
    """
    CivilizationMemory stores all timeline epoch blocks and append-only event logs.
    """
    def __init__(self):
        self.epochs = {}  # epoch_number -> Epoch
        self.event_stream = []

    def get_epoch(self, epoch_number):
        if epoch_number not in self.epochs:
            self.epochs[epoch_number] = Epoch(epoch_number)
        return self.epochs[epoch_number]

    def record_civilization_event(self, clock, event_type, actor_id, details=None):
        """
        Creates and stores a historical event inside both the global stream and local epoch segment.
        """
        epoch_num = clock.epoch
        event = HistoricalEvent(clock.cycle, epoch_num, event_type, actor_id, details)
        
        self.event_stream.append(event)
        epoch_obj = self.get_epoch(epoch_num)
        epoch_obj.log_event(event)
        
        return event
