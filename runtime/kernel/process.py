import uuid

class CognitiveProcess:
    """
    CognitiveProcess represents an execution thread context (Thread Control Block).
    """
    def __init__(self, program_lines, priority=1.0, goal="minimize_uncertainty"):
        self.process_id = str(uuid.uuid4())
        self.program = program_lines
        self.cip = 0
        self.registers = {
            "CR0": None,
            "CR1": None,
            "CR2": [],
            "CR3": None,
            "CR4": {"min": 0.0, "max": 1.0},
            "CR5": 100.0,
            "CR6": [],
            "CR7": 1.0,
            "CR8": {
                "goal": goal,
                "utility": "accuracy_max",
                "priority": priority,
                "constraints": {"uncertainty_limit": 0.3}
            }
        }
        self.status = "READY" # READY, RUNNING, SUSPENDED, TERMINATED
