class InterruptPolicy:
    """
    InterruptPolicy defines the severity levels and mapping routing rules for CPU exceptions.
    """
    @staticmethod
    def evaluate(interrupt_code):
        # Maps vector codes to severity levels (0: Info, 1: Warning, 2: Recoverable, 3: Critical, 4: Panic)
        severities = {
            "INT000": 0,  # Informational (System Boot)
            "INT001": 2,  # Recoverable (Contradiction Found)
            "INT002": 3,  # Critical (Resource Depleted)
            "INT003": 4,  # Kernel Panic (Lineage Violation)
            "INT004": 1,  # Warning (Uncertainty Explosion)
            "INT005": 4   # Kernel Panic (Memory Corruption)
        }
        
        severity = severities.get(interrupt_code, 1)
        
        # Policy Action Routing Selection
        if severity == 0:
            return {"severity": severity, "action": "LOG_INFO"}
        elif severity == 1:
            return {"severity": severity, "action": "LOG_WARNING"}
        elif severity == 2:
            return {"severity": severity, "action": "SPAWN_HANDLER_THREAD"}
        elif severity == 3:
            return {"severity": severity, "action": "SUSPEND_AND_REBALANCE"}
        elif severity == 4:
            return {"severity": severity, "action": "PANIC_AND_QUARANTINE"}
            
        return {"severity": severity, "action": "LOG_WARNING"}
