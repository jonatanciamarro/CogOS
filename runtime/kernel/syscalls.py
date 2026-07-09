class CognitiveSyscallHandler:
    """
    CognitiveSyscallHandler acts as the syscall mediator, enforcing E-WRITE / E-EVOLVE permissions.
    """
    @staticmethod
    def call(context, syscall_name, args):
        mode = context.state.mode
        if mode in ["QUARANTINED", "HALTED"]:
            raise PermissionError(f"CVM execution mode '{mode}' blocks syscall invocation.")
            
        if syscall_name == "SYS_OBSERVE":
            # Ingests raw signal into episodic memory
            sig_uri, ctx_uri = args[0], args[1]
            obs_uri = sig_uri.replace("signal", "observation")
            
            context.store_node("episodic", obs_uri, {
                "type": "Observation",
                "derived_from": sig_uri,
                "context": ctx_uri
            })
            return obs_uri
            
        elif syscall_name == "SYS_COMMIT_KNOWLEDGE":
            # Promotion of belief to knowledge
            belief_uri, evidence_uri = args[0], args[1]
            kn_uri = belief_uri.replace("belief", "knowledge")
            
            context.store_node("semantic", kn_uri, {
                "type": "Knowledge",
                "references": belief_uri,
                "evidence": evidence_uri
            })
            return kn_uri
            
        else:
            raise NotImplementedError(f"Syscall {syscall_name} not supported by the kernel.")
