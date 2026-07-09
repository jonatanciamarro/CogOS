import uuid

class CVMState:
    """
    CVMState holds the complete, unified operational state of the Cognitive Virtual Machine (CVM).
    No side effects or state changes may occur outside this central state tracker.
    """
    def __init__(self):
        # Unique machine execution session identifier
        self.session_id = str(uuid.uuid4())
        
        # Registers: CR0-CR8 (Pointers to LKB node URIs)
        self.registers = {
            "CR0": None,  # Context URI
            "CR1": None,  # Active Belief URI
            "CR2": [],    # Evidence Buffer (List of URIs)
            "CR3": None,  # Decision Candidate URI
            "CR4": {"min": 0.0, "max": 1.0}, # Uncertainty Interval
            "CR5": 100.0, # Resource Budget (Compute units/Energy)
            "CR6": [],    # Lineage Chain (List of URIs)
            "CR7": 1.0,   # Attention Vector
            "CR8": {      # Purpose Vector
                "goal": "minimize_uncertainty",
                "utility": "accuracy_max",
                "priority": 1.0,
                "constraints": {"uncertainty_limit": 0.3}
            }
        }
        
        # Graph Memory structure metadata total
        self.memory_metadata = {
            "node_count": 0,
            "relationship_count": 0,
            "graph_hash": "genesis_hash",
            "total_entropy": 1.0
        }
        
        # Execution Thread Table
        self.process_table = {}
        self.active_process_id = None
        
        # Interrupt Registers
        self.interrupt_flags = {
            "INT001": False, # Contradiction Found
            "INT002": False, # Resource Depleted
            "INT003": False, # Lineage Violation
            "INT004": False, # Uncertainty Explosion
            "INT005": False  # Memory Corruption
        }
        self.mode = "BOOT" # Modes: BOOT, RUNNING, WARNING, DEGRADED, QUARANTINED, RECOVERY, HALTED
        self.cip = 0       # Cognitive Instruction Pointer
        
    def copy(self):
        new_state = CVMState()
        new_state.session_id = self.session_id
        new_state.registers = {
            "CR0": self.registers["CR0"],
            "CR1": self.registers["CR1"],
            "CR2": list(self.registers["CR2"]),
            "CR3": self.registers["CR3"],
            "CR4": dict(self.registers["CR4"]),
            "CR5": self.registers["CR5"],
            "CR6": list(self.registers["CR6"]),
            "CR7": self.registers["CR7"],
            "CR8": dict(self.registers["CR8"])
        }
        new_state.memory_metadata = dict(self.memory_metadata)
        new_state.process_table = dict(self.process_table)
        new_state.active_process_id = self.active_process_id
        new_state.interrupt_flags = dict(self.interrupt_flags)
        new_state.mode = self.mode
        new_state.cip = self.cip
        return new_state
