class Task:
    """
    Task represents a unit of work with associated cost and priority metadata.
    """
    def __init__(self, task_id, agent_id, callable_fn, priority=1.0,
                 cost_estimate=10, urgency=1.0, expected_information_gain=1.0):
        self.id = task_id
        self.agent_id = agent_id
        self.fn = callable_fn
        self.priority = priority
        self.cost_estimate = cost_estimate
        self.urgency = urgency
        self.expected_information_gain = expected_information_gain

    @property
    def roi(self) -> float:
        return self.priority / max(1.0, self.cost_estimate)


class TaskQueue:
    """
    TaskQueue maintains a priority-ordered list of pending tasks.
    Tasks with higher ROI (priority / cost) are executed first.
    """
    def __init__(self):
        self._queue = []

    def enqueue(self, task: Task):
        self._queue.append(task)
        self._queue.sort(key=lambda t: -t.roi)

    def dequeue(self) -> Task:
        return self._queue.pop(0) if self._queue else None

    def __len__(self):
        return len(self._queue)
