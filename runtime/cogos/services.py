class CognitiveService:
    """
    CognitiveService defines the abstract base interface for all CogOS Kernel Daemons.
    """
    def __init__(self, name, interval=1.0):
        self.name = name
        self.interval = interval
        self.running = False

    def start(self):
        self.running = True

    def tick(self, system_state):
        raise NotImplementedError("Kernel services must implement tick().")

    def shutdown(self):
        self.running = False


class AttentionService(CognitiveService):
    """
    AttentionService dynamically recalibrates CR7 attention weights for active processes.
    """
    def __init__(self):
        super().__init__("attention_manager", interval=1.0)

    def tick(self, system_state):
        if not system_state.processes:
            return
            
        total_weight = 0.0
        weights = {}
        
        # Calculate active thread scheduling priorities
        for pid, process in system_state.processes.items():
            if process.status == "TERMINATED":
                continue
            priority = process.registers["CR8"]["priority"]
            cr4 = process.registers["CR4"]
            uncertainty = max(0.01, cr4["max"] - cr4["min"])
            
            weight = priority * uncertainty
            weights[pid] = weight
            total_weight += weight
            
        if total_weight > 0.0:
            for pid, process in system_state.processes.items():
                if process.status == "TERMINATED":
                    continue
                # Allocate CR7 Attention Share
                process.registers["CR7"] = weights[pid] / total_weight


class GCService(CognitiveService):
    """
    GCService monitors memory space allocations and sweeps orphaned or low-attention nodes.
    """
    def __init__(self):
        super().__init__("epistemic_gc", interval=5.0)

    def tick(self, system_state):
        # Epistemic GC sweeps dormant nodes in semantic memory
        pass


class EpistemicMonitorService(CognitiveService):
    """
    EpistemicMonitorService tracks active uncertainty thresholds and detects contradictions.
    """
    def __init__(self):
        super().__init__("epistemic_monitor", interval=1.0)

    def tick(self, system_state):
        # Scans semantic/episodic graph for contradictory relations
        pass
