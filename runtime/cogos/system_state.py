from runtime.core.cvm_state import CVMState

class CogOSSystemState:
    """
    CogOSSystemState acts as the unified system-wide state log.
    It links the CVM State, process registers, running daemons, and graph memory.
    """
    def __init__(self):
        # The virtual CPU state
        self.cpu_state = CVMState()
        
        # Thread process table (PIDs to CognitiveProcess objects)
        self.processes = {}
        self.active_pid = None
        
        # Active system services/daemons
        self.services = {}
        
        # Unified Property Graph memory database
        self.knowledge_graph = None
        
        # Real-time execution metrics
        self.metrics = {
            "total_cycles": 0,
            "interrupts_handled": 0,
            "contradictions_resolved": 0,
            "semantic_compression_ratio": 1.0,
            "lineage_preservation_score": 1.0
        }
        
        # Global OS status
        self.status = "BOOT"
