from runtime.cvm_engine.decoder import InstructionDecoder
from runtime.cvm_engine.executor import InstructionExecutor
from runtime.verifier.omega import RuntimeOmegaVerifier
from runtime.verifier.csa import RuntimeCSAVerifier
from runtime.verifier.ctt import RuntimeCTTVerifier

class CognitiveCPU:
    """
    CognitiveCPU implements the Fetch-Decode-Validate-Execute-Commit loop of the CVM processor.
    """
    def __init__(self, context):
        self.context = context
        self.program = []
        
    def load_program(self, program_lines):
        """
        Loads a list of raw CIL assembly instruction strings into memory.
        """
        self.program = program_lines
        self.context.state.cip = 0
        self.context.state.mode = "RUNNING"
        
    def fetch(self):
        """
        Fetches the CIL instruction from the program memory slot pointed by CIP.
        """
        cip = self.context.state.cip
        if cip < 0 or cip >= len(self.program):
            return None
        return self.program[cip]
        
    def step(self):
        """
        Executes a single step of the CVM CPU clock cycle.
        """
        if self.context.state.mode in ["HALTED", "QUARANTINED"]:
            return False
            
        raw_instruction = self.fetch()
        if raw_instruction is None:
            # End of program memory reached
            self.context.state.mode = "HALTED"
            return False
            
        decoded = InstructionDecoder.decode(raw_instruction)
        if decoded is None:
            # Empty or comment line, increment CIP and continue
            self.context.state.cip += 1
            return True
            
        # 1. Pre-Execution Validation (Epistemic Shield)
        RuntimeOmegaVerifier.validate(self.context, decoded)
        RuntimeCTTVerifier.validate(self.context, decoded)
        RuntimeCSAVerifier.validate(self.context, decoded)
        
        # 2. Execution & Commit
        InstructionExecutor.execute(self.context, decoded)
        
        # 3. Increment Instruction Pointer
        self.context.state.cip += 1
        return True
        
    def run(self):
        """
        Runs the loaded CIL program until a HALT instruction is hit or the budget yields.
        """
        while self.step():
            pass
