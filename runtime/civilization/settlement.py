class Settlement:
    """
    Settlement is a symbolic grouping of agents sharing local culture and knowledge.
    Settlements exchange memes and hypotheses via EventBus — no direct coupling.
    """
    def __init__(self, name: str):
        self.name = name
        self.population: list = []          # list[AgentProtocol]
        self.local_knowledge: list = []     # promoted hypotheses / theories
        self.local_memes: list = []

    def add_agent(self, agent) -> None:
        self.population.append(agent)

    def remove_agent(self, agent_id: str) -> None:
        self.population = [a for a in self.population
                           if a.identity.agent_id != agent_id]

    def tick(self, context) -> None:
        """Run one cognitive cycle for every active agent."""
        for agent in self.population:
            if hasattr(agent, "cognitive_cycle"):
                try:
                    agent.cognitive_cycle()
                except Exception:
                    pass  # individual agent failure never crashes the Settlement

    @property
    def population_size(self) -> int:
        return len(self.population)
