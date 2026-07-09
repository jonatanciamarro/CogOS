from runtime.core.omega_state import OmegaEngine

class InstructionExecutor:
    """
    InstructionExecutor processes CVM instructions, updates registers, and performs memory writes.
    """
    @staticmethod
    def execute(context, decoded_instruction):
        if not decoded_instruction:
            return
            
        opcode = decoded_instruction["opcode"]
        args = decoded_instruction["args"]
        
        # 1. Base Cost Calculation
        cost = 5.0
        if opcode in ["INFER", "ANALOGIZE", "PREDICT"]:
            cost = 50.0
        elif opcode in ["VERIFY", "RESOLVE_CONTRADICTION", "VERIFY_EVIDENCE"]:
            cost = 20.0
        elif opcode in ["MUTATE_MODEL", "SPLIT_CONCEPT", "MERGE_CONCEPT"]:
            cost = 100.0
        elif opcode in ["STORE", "RECALL", "COMMIT_STATE", "LOAD_STATE"]:
            cost = 10.0
            
        old_state = context.state.copy()
        
        # 2. Command Dispatching
        if opcode == "LOAD_CONTEXT":
            # args: [register, context_uri]
            reg, uri = args[0], args[1]
            context.state.registers[reg] = uri
            
        elif opcode == "LOAD_SIGNAL":
            # args: [register, signal_uri]
            reg, uri = args[0], args[1]
            context.state.registers[reg] = uri
            
        elif opcode == "LOAD_STATE":
            # args: [register, memory_uri]
            reg, uri = args[0], args[1]
            context.state.registers[reg] = uri
            
        elif opcode == "LOAD_BELIEF":
            # args: [register, belief_uri]
            reg, uri = args[0], args[1]
            context.state.registers[reg] = uri
            
        elif opcode == "OBSERVE":
            # args: [register_dest, signal_uri]
            reg_dest, sig_uri = args[0], args[1]
            obs_uri = sig_uri.replace("signal", "observation")
            
            # Store the observation node in episodic memory
            context.store_node("episodic", obs_uri, {
                "type": "Observation",
                "derived_from": sig_uri,
                "observer": context.state.registers["CR0"]
            })
            context.state.registers[reg_dest] = obs_uri
            
        elif opcode == "STORE":
            # args: [register_src, partition]
            reg_src, partition = args[0], args[1]
            uri = context.state.registers[reg_src]
            node = context.get_node(uri)
            if node:
                context.store_node(partition.lower(), uri, node)
                
        elif opcode == "COMMIT_STATE":
            # args: [register_src]
            reg_src = args[0]
            uri = context.state.registers[reg_src]
            node = context.get_node(uri)
            if node:
                context.store_node("semantic", uri, node)
                
        elif opcode == "VERIFY" or opcode == "VERIFY_EVIDENCE":
            # args: [register_dest, belief_register, evidence_register]
            reg_dest, reg_belief, reg_evidence = args[0], args[1], args[2]
            belief_uri = context.state.registers[reg_belief]
            evidence_uri = context.state.registers[reg_evidence]
            
            # Perform verification
            verified_uri = f"cse://evidence/{belief_uri.split('/')[-1]}_verified"
            context.store_node("episodic", verified_uri, {
                "type": "Evidence",
                "references": belief_uri,
                "weight": 0.85
            })
            
            context.state.registers[reg_dest] = verified_uri
            # Shift uncertainty interval (CR4)
            context.state.registers["CR4"]["min"] = min(0.9, context.state.registers["CR4"]["min"] + 0.1)
            # Add to lineage (CR6)
            if evidence_uri not in context.state.registers["CR6"]:
                context.state.registers["CR6"].append(evidence_uri)
            
        elif opcode == "COLLAPSE_STATE" or opcode == "COLLAPSE_DECISION":
            # args: [register_dest, belief_register, evidence_register]
            reg_dest, reg_belief, reg_evidence = args[0], args[1], args[2]
            belief_uri = context.state.registers[reg_belief]
            evidence_uri = context.state.registers[reg_evidence]
            
            dec_uri = belief_uri.replace("belief", "decision")
            context.store_node("semantic", dec_uri, {
                "type": "Decision",
                "evidence": evidence_uri,
                "lineage": list(context.state.registers["CR6"])
            })
            context.state.registers[reg_dest] = dec_uri
            
        elif opcode == "RESOLVE_CONTRADICTION":
            # args: [register_dest, H1_register, H2_register]
            reg_dest, reg_h1, reg_h2 = args[0], args[1], args[2]
            h1_uri = context.state.registers[reg_h1]
            h2_uri = context.state.registers[reg_h2]
            
            # Arbitrates and selects the second hypothesis as evolved replacement
            resolved_uri = h2_uri
            context.state.registers[reg_dest] = resolved_uri
            
            # Append predecessor to lineage traces (CR6)
            if h1_uri and h1_uri not in context.state.registers["CR6"]:
                context.state.registers["CR6"].append(h1_uri)
            
        elif opcode == "ALLOCATE_ATTENTION":
            # args: [register, value]
            reg, val = args[0], float(args[1])
            context.state.registers[reg] = val
            
        elif opcode == "DEBIT_RESOURCE":
            # args: [register, value]
            reg, val = args[0], float(args[1])
            context.state.registers[reg] = max(0.0, context.state.registers[reg] - val)
            
        elif opcode == "HALT" or opcode == "HALT_REASON":
            reason = args[0] if args else "Normal Halt"
            context.state.mode = "HALTED"
            
        # 3. Apply state transitions and verify conservation constraints
        OmegaEngine.transition(old_state, context.state, cost)
