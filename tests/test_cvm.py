import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.core.machine_context import MachineContext
from runtime.cvm_engine.cpu import CognitiveCPU

class TestCVMExecution(unittest.TestCase):
    """
    Test suite for verifying Cognitive Type Theory (CTT), CSA Lineage, and CVM instruction steps.
    """
    def test_boot_and_genesis_execution(self):
        context = MachineContext()
        cpu = CognitiveCPU(context)
        
        program = [
            "LOAD_CONTEXT CR0, cse://context/genesis",
            "LOAD_SIGNAL CR2, cse://signal/sky_color",
            "OBSERVE CR1, cse://signal/sky_color",
            "STORE CR1, semantic",
            "VERIFY CR2, CR1, CR2",
            "COMMIT_STATE CR1",
            "HALT"
        ]
        
        cpu.load_program(program)
        cpu.run()
        
        self.assertEqual(context.state.mode, "HALTED")
        self.assertEqual(context.state.registers["CR0"], "cse://context/genesis")
        self.assertEqual(context.state.registers["CR1"], "cse://observation/sky_color")
        self.assertIn("cse://signal/sky_color", context.state.registers["CR6"])
        
    def test_ctt_type_leap_protection(self):
        context = MachineContext()
        cpu = CognitiveCPU(context)
        
        # Prohibited: Direct leap from Signal to Decision collapse without verification
        program = [
            "LOAD_CONTEXT CR0, cse://context/temp",
            "LOAD_SIGNAL CR1, cse://signal/direct_sig",
            "COLLAPSE_DECISION CR3, CR1, CR2",
            "HALT"
        ]
        cpu.load_program(program)
        
        with self.assertRaises(TypeError):
            cpu.run()
            
    def test_csa_lineage_protection(self):
        context = MachineContext()
        cpu = CognitiveCPU(context)
        
        # Prohibited: Decision collapse without lineage logs (CR6 is empty)
        program = [
            "LOAD_CONTEXT CR0, cse://context/temp",
            "LOAD_BELIEF CR1, cse://belief/unfounded_belief",
            "LOAD_STATE CR2, cse://evidence/active_evidence",
            "COLLAPSE_DECISION CR3, CR1, CR2",
            "HALT"
        ]
        cpu.load_program(program)
        
        with self.assertRaises(ValueError):
            cpu.run()
        self.assertEqual(context.state.mode, "QUARANTINED")

if __name__ == "__main__":
    unittest.main()
