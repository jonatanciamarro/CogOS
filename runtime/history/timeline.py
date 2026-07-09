class CognitiveClock:
    """
    CognitiveClock manages absolute cycles, epochs, and generations.
    """
    def __init__(self, cycles_per_epoch=100, epochs_per_generation=5):
        self.cycle = 0
        self.cycles_per_epoch = cycles_per_epoch
        self.epochs_per_generation = epochs_per_generation

    def tick(self, count=1):
        """
        Increments absolute execution cycles.
        """
        self.cycle += count
        return self.cycle

    @property
    def epoch(self):
        return self.cycle // self.cycles_per_epoch

    @property
    def generation(self):
        return self.epoch // self.epochs_per_generation
