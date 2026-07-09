from enum import Enum, auto


class KernelState(Enum):
    BOOT        = auto()
    RUNNING     = auto()
    PAUSED      = auto()
    STOPPED     = auto()
    FAILED      = auto()
    HIBERNATING = auto()


class SimulationKernel:
    """
    SimulationKernel is the state machine that controls the simulation lifecycle.
    SimulationLoop checks kernel.running — it never controls state directly.

    Transitions:
        BOOT → RUNNING
        RUNNING ⇄ PAUSED
        RUNNING → STOPPED
        RUNNING → FAILED
        RUNNING ⇄ HIBERNATING
    """
    def __init__(self):
        self.state = KernelState.BOOT
        self._tick_count = 0

    @property
    def running(self) -> bool:
        return self.state == KernelState.RUNNING

    def start(self):
        if self.state == KernelState.BOOT:
            self.state = KernelState.RUNNING

    def pause(self):
        if self.state == KernelState.RUNNING:
            self.state = KernelState.PAUSED

    def resume(self):
        if self.state in (KernelState.PAUSED, KernelState.HIBERNATING):
            self.state = KernelState.RUNNING

    def stop(self):
        self.state = KernelState.STOPPED

    def hibernate(self):
        if self.state == KernelState.RUNNING:
            self.state = KernelState.HIBERNATING

    def fail(self, reason: str = ""):
        self.state = KernelState.FAILED
        self._failure_reason = reason

    def tick(self) -> int:
        self._tick_count += 1
        return self._tick_count
