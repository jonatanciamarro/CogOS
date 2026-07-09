from runtime.hardware.interrupt_policy import InterruptPolicy
from runtime.kernel.process import CognitiveProcess

class InterruptController:
    """
    InterruptController dispatches hardware/epistemic exceptions to correct handlers and spawns recovery threads.
    """
    def __init__(self, kernel):
        self.kernel = kernel

    def trigger(self, interrupt_code):
        """
        Receives an interrupt flag, audits its policy severity, and directs system response.
        """
        policy_result = InterruptPolicy.evaluate(interrupt_code)
        action = policy_result["action"]
        severity = policy_result["severity"]
        
        self.kernel.system_state.metrics["interrupts_handled"] += 1
        
        if action == "SPAWN_HANDLER_THREAD":
            # Recoverable anomaly (INT001 Contradiction). Spawn dynamic handler thread on CVM.
            handler_program = [
                "// --- Interrupt Handler Thread ---",
                "LOAD_CONTEXT CR0, cse://context/arbitration_solver",
                "RESOLVE_CONTRADICTION CR3, CR1, CR2",
                "COMMIT_STATE CR3",
                "HALT_REASON contradiction_resolved"
            ]
            
            handler_process = CognitiveProcess(handler_program, priority=3.0, goal="resolve_contradiction")
            
            # Map faulted process registers directly into handler registers
            handler_process.registers["CR1"] = self.kernel.context.state.registers["CR1"]
            handler_process.registers["CR2"] = list(self.kernel.context.state.registers["CR2"])
            handler_process.status = "READY"
            
            # Suspend active thread, load handler
            active_pid = self.kernel.system_state.active_pid
            if active_pid:
                self.kernel.system_state.processes[active_pid].status = "SUSPENDED"
                
            self.kernel.spawn_process(handler_process)
            
        elif action == "SUSPEND_AND_REBALANCE":
            # Suspend current context and trigger resource cleanups (INT002 Resource Depleted)
            active_pid = self.kernel.system_state.active_pid
            if active_pid:
                self.kernel.system_state.processes[active_pid].status = "SUSPENDED"
            self.kernel.schedule_next()
            
        elif action == "PANIC_AND_QUARANTINE":
            # Freeze execution. Lock Graph Memory read-only (INT003 / INT005)
            self.kernel.context.state.mode = "QUARANTINED"
            self.kernel.system_state.status = "QUARANTINED"
            active_pid = self.kernel.system_state.active_pid
            if active_pid:
                self.kernel.system_state.processes[active_pid].status = "SUSPENDED"
