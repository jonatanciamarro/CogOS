from runtime.bus.event_bus import CogOSEvents, EventPriority

class Executor:
    """
    Executor runs tasks from the TaskQueue, checking BudgetResult before execution.
    Reacts differently per resource deficit type; emits typed events via EventBus.
    """
    def __init__(self, task_queue, agents_by_id: dict, event_bus=None):
        self.queue = task_queue
        self.agents = agents_by_id
        self.bus = event_bus

    def run_next(self) -> bool:
        """
        Dequeues and executes the next task if the agent has sufficient resources.
        Returns True if a task was executed.
        """
        task = self.queue.dequeue()
        if task is None:
            return False

        agent = self.agents.get(task.agent_id)
        if agent is None:
            return False

        budget = getattr(agent, "resource_budget", None)
        if budget is None:
            task.fn()
            return True

        result = budget.consume("cpu", task.cost_estimate)

        if result.ok:
            task.fn()
            if self.bus:
                self.bus.publish(CogOSEvents.RESOURCE_ALLOCATED, {
                    "agent_id": task.agent_id, "task_id": task.id
                }, EventPriority.NORMAL)
            return True

        # React per deficit type
        if self.bus:
            self.bus.publish(CogOSEvents.BUDGET_EXHAUSTED, {
                "agent_id": task.agent_id,
                "status":   result.status,
                "deficit":  result.deficit
            }, EventPriority.CRITICAL)

        if result.status == "INSUFFICIENT_ENERGY":
            # Hibernate: re-enqueue for later
            self.queue.enqueue(task)

        # INSUFFICIENT_CPU → skip (wait for daemon replenishment)
        # INSUFFICIENT_MEMORY → skip (swap handled externally)
        # INSUFFICIENT_ATTENTION → skip (replanning handled externally)
        return False
