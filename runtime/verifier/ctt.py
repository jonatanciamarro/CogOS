class RuntimeCTTVerifier:
    """
    RuntimeCTTVerifier performs dynamic type-safety checks before instruction execution.
    """
    @staticmethod
    def validate(context, decoded_instruction):
        if not decoded_instruction:
            return
            
        opcode = decoded_instruction["opcode"]
        args = decoded_instruction["args"]
        
        # Ensure direct Signal -> Decision leaps are blocked
        if opcode in ["COLLAPSE_STATE", "COLLAPSE_DECISION"]:
            reg_belief = args[1]
            belief_uri = context.state.registers[reg_belief]
            
            # If trying to collapse something that is not a belief (like a raw signal), fail
            if not belief_uri or "signal" in belief_uri:
                raise TypeError("CSE-TYPE-001: Illegal epistemic transition. Decision requires validated Belief/Knowledge state.")
                
        # Ensure context references are correct
        if opcode == "OBSERVE":
            sig_uri = args[1]
            if "signal" not in sig_uri:
                raise TypeError("CSE-TYPE-003: Observer Frame/Signal source missing. Observation requires Signal input.")
