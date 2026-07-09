from runtime.economy.scheduling_policy import GreedyPolicy

class ResourceScheduler:
    """
    ResourceScheduler allocates CPU slices to competing agents using an injected SchedulingPolicy.
    """
    def __init__(self, policy=None):
        self.policy = policy or GreedyPolicy()

    def rank_tasks(self, tasks, agents_by_id: dict) -> list:
        """
        Returns tasks sorted by policy score descending.
        """
        def task_score(task):
            agent = agents_by_id.get(task.agent_id)
            if agent is None:
                return 0.0
            return self.policy.score(task, agent)

        return sorted(tasks, key=task_score, reverse=True)

    def allocate_cpu_slice(self, agent_list, total_cpu: int) -> dict:
        """
        Distributes total_cpu proportionally by agent trust_score.
        Returns dict: agent_id -> allocated_cpu
        """
        total_trust = sum(getattr(a, "trust_score", 0.5) for a in agent_list)
        if total_trust == 0:
            total_trust = len(agent_list) or 1

        allocation = {}
        for agent in agent_list:
            trust = getattr(agent, "trust_score", 0.5)
            allocation[agent.identity.agent_id] = int((trust / total_trust) * total_cpu)
        return allocation
