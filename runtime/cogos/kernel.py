from runtime.cogos.system_state import CogOSSystemState
from runtime.cogos.service_registry import ServiceRegistry
from runtime.cogos.services import AttentionService, GCService, EpistemicMonitorService
from runtime.cvm_engine.cpu import CognitiveCPU

class CogOSKernel:
    """
    CogOSKernel orchestrates the multitasking operating environment, loading programs,
    swapping register contexts, and ticking background system daemons.
    """
    def __init__(self, context):
        self.context = context
        self.system_state = CogOSSystemState()
        self.system_state.knowledge_graph = context
        
        self.service_registry = ServiceRegistry()
        self.cpu = CognitiveCPU(context)
        
        from runtime.hardware.interrupt_controller import InterruptController
        self.interrupt_controller = InterruptController(self)
        
        # Load core OS daemons
        self.service_registry.register(AttentionService())
        self.service_registry.register(GCService())
        self.service_registry.register(EpistemicMonitorService())

    def start(self):
        self.system_state.status = "RUNNING"
        self.service_registry.start_all()

    def spawn_process(self, process):
        """
        Loads a new CognitiveProcess thread into the operating process table.
        """
        self.system_state.processes[process.process_id] = process
        if not self.system_state.active_pid:
            self.system_state.active_pid = process.process_id
            process.status = "RUNNING"
            self.cpu.load_program(process.program)

    def tick(self):
        """
        Executes a single operating system tick cycle: ticks services, dispatches CPU,
        and saves thread control blocks back to memory.
        """
        if self.system_state.status != "RUNNING":
            return
            
        # 1. Tick background system services
        self.service_registry.tick_all(self.system_state)
        
        # 2. Swap thread registers and step active CPU
        active_pid = self.system_state.active_pid
        if active_pid:
            process = self.system_state.processes[active_pid]
            
            # Map thread TCB context directly onto active CVM CPU
            self.context.state.registers = process.registers
            self.context.state.cip = process.cip
            self.context.state.mode = process.status
            
            try:
                # Run one instruction cycle step
                cpu_stepped = self.cpu.step()
                
                # Check for flagged interrupts
                for intr, flagged in self.context.state.interrupt_flags.items():
                    if flagged:
                        self.interrupt_controller.trigger(intr)
                        self.context.state.interrupt_flags[intr] = False
            except Exception as e:
                if self.context.state.interrupt_flags.get("INT003"):
                    self.interrupt_controller.trigger("INT003")
                    self.context.state.interrupt_flags["INT003"] = False
                raise e
            
            # Save updated CPU state parameters back to TCB
            process.registers = self.context.state.registers
            process.cip = self.context.state.cip
            process.status = self.context.state.mode
            
            self.system_state.metrics["total_cycles"] += 1
            
            if not cpu_stepped or process.status in ["HALTED", "TERMINATED"]:
                process.status = "TERMINATED"
                self.schedule_next()

    def schedule_next(self):
        """
        Task scheduling dispatch: selects the next READY thread.
        """
        for pid, process in self.system_state.processes.items():
            if process.status == "READY":
                self.system_state.active_pid = pid
                process.status = "RUNNING"
                self.cpu.load_program(process.program)
                self.cpu.context.state.cip = process.cip
                return
        self.system_state.active_pid = None

    def shutdown(self):
        self.system_state.status = "HALTED"
        self.service_registry.shutdown_all()
