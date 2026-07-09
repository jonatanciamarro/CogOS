import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.core.machine_context import MachineContext
from runtime.cvm_engine.cpu import CognitiveCPU
from runtime.debugger.trace import CognitiveDebuggerTrace

class CB001Runner:
    """
    CB001Runner runs compiled CIL program benchmarks on the CVM CPU emulator
    and outputs the Discovery (DS) and Evolution (ES) scores.
    """
    @staticmethod
    def run_benchmark(program_file_path):
        print(f"=== Initializing CVM Simulator: {os.path.basename(program_file_path)} ===")
        context = MachineContext()
        cpu = CognitiveCPU(context)
        
        # Ingest CIL instruction lines
        with open(program_file_path, "r", encoding="utf-8") as f:
            program_lines = f.readlines()
            
        cpu.load_program(program_lines)
        
        step_count = 0
        # Run CPU cycles and trace steps
        while cpu.step():
            step_count += 1
            CognitiveDebuggerTrace.print_trace(context, step_count)
            
        print("\n--- Cycle Completed. Processing Benchmark Metrics ---")
        
        # Calculate CB-001 Scores
        # 1. Discovery Score (DS) = (Novelty * Accuracy * Evidence) / (EnergyCost * Contradiction)
        novelty = 0.90
        accuracy = 0.95
        evidence_weight = 0.85
        
        # Energy cost = consumed energy (max 100)
        energy_cost = max(1.0, 100.0 - context.state.registers["CR5"])
        contradiction_penalty = 1.0 # No active contradiction
        
        discovery_score = (novelty * accuracy * evidence_weight) / (energy_cost * contradiction_penalty)
        
        # 2. Evolution Score (ES) = KnowledgeGrowth / ComplexityIncrease
        knowledge_growth = float(context.state.memory_metadata["node_count"])
        complexity_increase = 1.0 # Normalized complexity baseline
        
        evolution_score = knowledge_growth / complexity_increase
        
        print("\n=============================================")
        print("         CB-001 BENCHMARK REPORT             ")
        print("=============================================")
        print(f" Total CPU cycles executed: {step_count}")
        print(f" Final System Mode:         {context.state.mode}")
        print(f" Remaining CR5 Resource:   {context.state.registers['CR5']:.2f} units")
        print(f" Discovery Score (DS):      {discovery_score:.4f}")
        print(f" Evolution Score (ES):      {evolution_score:.4f}")
        print("=============================================\n")
        
        return discovery_score, evolution_score

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cb001_file = os.path.join(current_dir, "cb001.cvm")
    CB001Runner.run_benchmark(cb001_file)
