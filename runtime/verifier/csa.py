class RuntimeCSAVerifier:
    """
    RuntimeCSAVerifier validates that Cognitive Single Assignment (CSA) rules and lineage logs are intact.
    """
    @staticmethod
    def validate(context, decoded_instruction):
        if not decoded_instruction:
            return
            
        opcode = decoded_instruction["opcode"]
        args = decoded_instruction["args"]
        
        # Every decision collapse must carry non-empty lineage pointers (CR6)
        if opcode in ["COLLAPSE_STATE", "COLLAPSE_DECISION"]:
            lineage = context.state.registers["CR6"]
            if not lineage or len(lineage) == 0:
                # Trigger Lineage Violation interrupt
                context.state.interrupt_flags["INT003"] = True
                context.state.mode = "QUARANTINED"
                raise ValueError("CSE-CONSTRAINT-003: Lineage path missing. Every knowledge node requires CSA lineage verification.")
