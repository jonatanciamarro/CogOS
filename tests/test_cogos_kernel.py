import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.cogos.boot import CogOSBootloader
from runtime.kernel.process import CognitiveProcess

class TestCogOSKernel(unittest.TestCase):
    """
    Test suite for verifying multitasking dispatching, scheduler attention,
    and interrupt routing policies inside the CogOS Kernel.
    """
    def test_kernel_boot_and_process_dispatch(self):
        kernel = CogOSBootloader.boot()
        self.assertEqual(kernel.system_state.status, "RUNNING")
        
        program = [
            "LOAD_CONTEXT CR0, cse://context/test",
            "LOAD_SIGNAL CR2, cse://signal/sensor_x",
            "OBSERVE CR1, cse://signal/sensor_x",
            "HALT"
        ]
        
        proc = CognitiveProcess(program, priority=1.0, goal="test_goal")
        kernel.spawn_process(proc)
        
        # Tick the kernel loop until the process finishes
        cycles = 0
        while kernel.system_state.active_pid and cycles < 20:
            kernel.tick()
            cycles += 1
            
        self.assertEqual(proc.status, "TERMINATED")
        self.assertIsNone(kernel.system_state.active_pid)

    def test_multitasking_scheduler_attention(self):
        kernel = CogOSBootloader.boot()
        
        p1 = CognitiveProcess(["LOAD_CONTEXT CR0, cse://ctx/1", "HALT"], priority=3.0, goal="high_prio")
        p2 = CognitiveProcess(["LOAD_CONTEXT CR0, cse://ctx/2", "HALT"], priority=1.0, goal="low_prio")
        
        kernel.spawn_process(p1)
        kernel.spawn_process(p2)
        
        # Execute tick to run the AttentionService and calculate CR7
        kernel.tick()
        
        # P1 priority (3.0) is higher than P2 priority (1.0). CR7 must be greater.
        self.assertGreater(p1.registers["CR7"], p2.registers["CR7"])

    def test_interrupt_controller_panic(self):
        kernel = CogOSBootloader.boot()
        
        # Prohibited: Decision collapse without lineage triggers INT003 (Panic & Quarantine)
        program = [
            "LOAD_CONTEXT CR0, cse://context/temp",
            "LOAD_BELIEF CR1, cse://belief/test_belief",
            "LOAD_STATE CR2, cse://evidence/active_evidence",
            "COLLAPSE_DECISION CR3, CR1, CR2",
            "HALT"
        ]
        
        proc = CognitiveProcess(program, priority=1.0, goal="test_panic")
        kernel.spawn_process(proc)
        
        # Executing instructions
        try:
            for _ in range(5):
                kernel.tick()
        except ValueError:
            pass # Expect lineage exception
            
        # The Interrupt Controller must transition kernel state to QUARANTINED
        self.assertEqual(kernel.system_state.status, "QUARANTINED")

if __name__ == "__main__":
    unittest.main()
