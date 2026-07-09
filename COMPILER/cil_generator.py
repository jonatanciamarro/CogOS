class CILGenerator:
    """
    CILGenerator translates parsed CSEL blocks into linear CIL assembly text instructions.
    """
    @staticmethod
    def generate(entities):
        instructions = []
        instructions.append("// --- CIL Bytecode Header ---")
        
        for name, properties in entities.items():
            identity = properties.get("IDENTITY", f"cse://concept/{name.lower()}")
            instructions.append(f"// Compiling entity: {name}")
            instructions.append(f"LOAD_CONTEXT CR0, {identity}")
            
            transformation = properties.get("TRANSFORMATION", "")
            
            if "Signal" in transformation:
                # Lowering step to load and observe
                instructions.append("LOAD_SIGNAL CR2, cse://signal/sensor_input")
                instructions.append("OBSERVE CR1, cse://signal/sensor_input")
                
            if "Belief" in transformation or "Context" in transformation:
                instructions.append("LOAD_BELIEF CR1, cse://belief/speculative_state")
                
            if "Evidence" in transformation:
                instructions.append("VERIFY_EVIDENCE CR4, CR1, CR2")
                
            if "Decision" in transformation:
                instructions.append("COLLAPSE_DECISION CR3, CR1, CR2")
                instructions.append("COMMIT_STATE CR3")
                
        instructions.append("HALT_REASON goal_achieved")
        return instructions
