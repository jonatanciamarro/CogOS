class SocietyManager:
    """
    SocietyManager tracks population registrations, censes, and metric summaries.
    """
    def __init__(self):
        self.population = {}  # agent_id -> agent_object

    def register_agent(self, agent):
        """
        Adds a new CognitiveAgent to the active society table.
        """
        self.population[agent.identity.agent_id] = agent

    def deregister_agent(self, agent_id):
        """
        Removes an agent from active society participation.
        """
        self.population.pop(agent_id, None)

    def get_census_summary(self):
        return {
            "population_size": len(self.population),
            "active_agents": [agent.name for agent in self.population.values()]
        }
