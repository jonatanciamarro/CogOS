class RuntimeOmegaVerifier:
    """
    RuntimeOmegaVerifier handles pre-execution verification of Omega constraints (like resource budget CR5 bounds).
    """
    @staticmethod
    def validate(context, decoded_instruction):
        if not decoded_instruction:
            return
            
        # Check if the execution budget is depleted before starting the cycle
        budget = context.state.registers["CR5"]
        if budget <= 0.0:
            context.state.interrupt_flags["INT002"] = True
            context.state.mode = "DEGRADED"
            raise ValueError("CSE-RESOURCE-002: CR5 Resource Budget fully depleted. Cannot execute instruction.")
            
        # Check if attention is too low
        attention = context.state.registers["CR7"]
        if attention < 0.10:
            raise ValueError("CSE-RESOURCE-003: Thread attention level (CR7) too low for execution.")
