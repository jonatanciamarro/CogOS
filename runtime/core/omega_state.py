class OmegaState:
    """
    OmegaState represents the global dynamic vector Ω_t.
    """
    def __init__(self):
        self.identity_hash = "genesis"
        self.context_bound = "global"
        self.memory_footprint = 0
        self.knowledge_weight = 0.0
        self.belief_count = 0
        self.uncertainty = 1.0
        self.trust_factor = 1.0
        self.energy_budget = 100.0
        self.purpose_priority = 1.0

    def copy(self):
        new_omega = OmegaState()
        new_omega.identity_hash = self.identity_hash
        new_omega.context_bound = self.context_bound
        new_omega.memory_footprint = self.memory_footprint
        new_omega.knowledge_weight = self.knowledge_weight
        new_omega.belief_count = self.belief_count
        new_omega.uncertainty = self.uncertainty
        new_omega.trust_factor = self.trust_factor
        new_omega.energy_budget = self.energy_budget
        new_omega.purpose_priority = self.purpose_priority
        return new_omega


class OmegaEngine:
    """
    OmegaEngine executes state transition rules and checks the Conservation Law.
    """
    @staticmethod
    def transition(old_state, new_state, cost):
        """
        Transition function: Ω_t+1 = F(Ω_t, O_t, A_t, Λ)
        Updates the values of Omega based on registry modifications.
        """
        old_omega = old_state.registers["CR4"]
        new_omega = new_state.registers["CR4"]
        
        # Calculate uncertainty interval width
        u_old = old_omega["max"] - old_omega["min"]
        u_new = new_omega["max"] - new_omega["min"]
        
        # Resource deduction
        new_state.registers["CR5"] = max(0.0, old_state.registers["CR5"] - cost)
        
        # Check conservation law
        if not OmegaEngine.conservation_check(old_state, new_state, cost):
            # If conservation is breached, force an error by throwing an exception
            raise ValueError("CSE-CONSERVATION-001: Cognitive Conservation Law breached.")

    @staticmethod
    def conservation_check(old_state, new_state, cost):
        """
        Cognitive Conservation Equation:
        ΔL + ΔK + ΔU + ΔC + ΔE_v >= 0
        """
        # 1. Delta Lineage: Trace chain length
        delta_l = len(new_state.registers["CR6"]) - len(old_state.registers["CR6"])
        
        # 2. Delta Knowledge: Concept counts
        delta_k = new_state.memory_metadata["node_count"] - old_state.memory_metadata["node_count"]
        
        # 3. Delta Uncertainty (reduction of uncertainty is positive epistemic progress)
        u_old = old_state.registers["CR4"]["max"] - old_state.registers["CR4"]["min"]
        u_new = new_state.registers["CR4"]["max"] - new_state.registers["CR4"]["min"]
        delta_u = u_old - u_new  # Positive if uncertainty decreased
        
        # 4. Computational Cost (transition cost is positive input energy)
        delta_c = cost
        
        # 5. Evolution Value (evaporating old nodes without losing lineage yields positive E_v)
        delta_ev = 0.0
        if delta_k < 0:
            delta_ev = float(abs(delta_k)) * 2.0
            
        # Overall balance equation
        balance = delta_l + delta_k + delta_u + delta_c + delta_ev
        return balance >= 0.0
