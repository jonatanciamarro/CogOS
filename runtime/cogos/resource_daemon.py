from runtime.bus.event_bus import CogOSEvents, EventPriority

class ResourceDaemon:
    """
    ResourceDaemon runs periodic resource maintenance tasks at each clock tick:
    replenishes energy, runs GC on idle hypotheses, and emits RESOURCE_UPDATED.
    """
    def __init__(self, event_bus=None, energy_replenish=5, memory_replenish=20):
        self.bus = event_bus
        self.energy_replenish = energy_replenish
        self.memory_replenish = memory_replenish

    def tick(self, agents_by_id: dict, idea_market=None):
        """
        Called once per CognitiveClock tick. Maintains all registered agents.
        """
        for agent_id, agent in agents_by_id.items():
            budget = getattr(agent, "resource_budget", None)
            if budget is None:
                continue

            from runtime.agents.agent_state import AgentLifecycleState
            if agent.lifecycle_state == AgentLifecycleState.ACTIVE:
                budget.replenish("energy", self.energy_replenish)
            elif agent.lifecycle_state == AgentLifecycleState.SUSPENDED:
                budget.replenish("memory", self.memory_replenish)

        # GC idle hypotheses in IdeaMarket
        if idea_market and self.bus:
            idea_market.tick_idle(self.bus)

        # Notify all subscribers that resources were replenished
        if self.bus:
            self.bus.publish(CogOSEvents.RESOURCE_UPDATED,
                             {"agent_count": len(agents_by_id)},
                             EventPriority.HIGH)
