class InstructionDecoder:
    """
    InstructionDecoder parses CIL assembly instruction strings into executable dictionaries.
    """
    @staticmethod
    def decode(instruction_str):
        if not instruction_str:
            return None
            
        clean_line = instruction_str.strip()
        
        # Skip empty lines and comment lines
        if not clean_line or clean_line.startswith("//") or clean_line.startswith("#"):
            return None
            
        parts = clean_line.split(None, 1)
        opcode = parts[0]
        args = []
        
        if len(parts) > 1:
            # Arguments are comma-separated
            args = [arg.strip() for arg in parts[1].split(",")]
            
        return {
            "opcode": opcode,
            "args": args
        }
