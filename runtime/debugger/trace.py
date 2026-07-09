class CognitiveDebuggerTrace:
    """
    CognitiveDebuggerTrace handles logging, trace printing, and runtime state observation.
    """
    @staticmethod
    def print_trace(context, step_count):
        state = context.state
        print(f"\n[CVM DEBUG] Cycle: {step_count:06d} | Mode: {state.mode}")
        print(f"  CIP: {state.cip}")
        print(f"  CR0 Context: {state.registers['CR0']}")
        print(f"  CR1 Belief:  {state.registers['CR1']}")
        print(f"  CR2 Evidence:{state.registers['CR2']}")
        print(f"  CR3 Decision:{state.registers['CR3']}")
        print(f"  CR4 Uncertainty Interval: [{state.registers['CR4']['min']:.2f}, {state.registers['CR4']['max']:.2f}]")
        print(f"  CR5 Budget:  {state.registers['CR5']:.2f} units")
        print(f"  CR6 Lineage: {state.registers['CR6']}")
        print(f"  CR7 Attention: {state.registers['CR7']:.2f}")
        print(f"  CR8 Purpose Goal: {state.registers['CR8']['goal']}")
