import sys

class CogOSShell:
    """
    CogOSShell implements the interactive REPL CLI loop for executing, monitoring,
    and debugging process threads and state registers inside the CVM kernel.
    """
    def __init__(self, kernel):
        self.kernel = kernel

    def execute_command(self, cmd_line):
        if not cmd_line:
            return ""
            
        parts = cmd_line.strip().split()
        if not parts:
            return ""
            
        cmd = parts[0].lower()
        
        if cmd == "status":
            state = self.kernel.system_state
            cpu = self.kernel.cpu.context.state
            output = [
                "=============================================",
                f" COGOS STATUS REPORT | Kernel: {state.status}",
                "=============================================",
                f" Active Process PID:  {state.active_pid}",
                f" Active CPU Mode:     {cpu.mode}",
                f" CPU Instruction Ptr: {cpu.cip}",
                f" Total Clock Cycles:  {state.metrics['total_cycles']}",
                f" Interrupts Handled:  {state.metrics['interrupts_handled']}",
                f" In Uncertainty:      [{cpu.registers['CR4']['min']:.2f}, {cpu.registers['CR4']['max']:.2f}]",
                "============================================="
            ]
            return "\n".join(output)
            
        elif cmd == "processes":
            output = ["=== Cognitive Process Table ==="]
            for pid, process in self.kernel.system_state.processes.items():
                output.append(f" PID: {pid[:8]}... | Status: {process.status:10s} | Goal: {process.registers['CR8']['goal']}")
            return "\n".join(output)
            
        elif cmd == "inspect":
            if len(parts) < 2:
                return "Usage: inspect [CR0-CR8]"
            reg_name = parts[1].upper()
            cpu_state = self.kernel.cpu.context.state
            if reg_name in cpu_state.registers:
                return f"{reg_name}: {cpu_state.registers[reg_name]}"
            return f"Register '{reg_name}' not found."
            
        elif cmd == "step":
            self.kernel.tick()
            return "System Ticked (1 clock cycle executed)."
            
        elif cmd == "run":
            cycles = 0
            while self.kernel.system_state.active_pid and cycles < 100:
                self.kernel.tick()
                cycles += 1
            return f"Execution loop finished. {cycles} clock cycles executed."
            
        elif cmd == "exit":
            return "exit"
            
        return f"Unknown command: '{cmd}'. Available: status, processes, inspect, step, run, exit."

    def start_loop(self):
        print("=============================================")
        print("     CogOS v0.1 Interactive Shell REPL       ")
        print("=============================================")
        print("Available Commands: status, processes, inspect [reg], step, run, exit\n")
        
        while True:
            try:
                line = input("cogos> ")
                result = self.execute_command(line)
                if result == "exit":
                    break
                if result:
                    print(result)
            except (KeyboardInterrupt, EOFError):
                print("\nShutting down CogOS Shell...")
                break
