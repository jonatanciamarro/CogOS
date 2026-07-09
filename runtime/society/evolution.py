from runtime.agents.capability import Capability

class EvolutionEngine:
    """
    EvolutionEngine audits uncertainty metrics to trigger adaptive spawning of specialized agents.
    """
    def __init__(self, lifecycle_manager):
        self.lifecycle_manager = lifecycle_manager

    def check_evolution_trigger(self, system_uncertainty, parent_agent=None):
        """
        Spawns a specialized solver child agent if global uncertainty exceeds 0.60 threshold.
        """
        if system_uncertainty > 0.60:
            child = self.lifecycle_manager.spawn_agent(
                "SpecializedSolverAgent", 
                parent_agent, 
                "uncertainty_mitigation"
            )
            # Give child evolve capabilities and tools
            child.add_capability(Capability("exploring", "E-READ"))
            self.lifecycle_manager.activate_agent(child.identity.agent_id)
            return child

        return None
