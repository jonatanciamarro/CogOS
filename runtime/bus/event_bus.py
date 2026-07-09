from enum import IntEnum

class EventPriority(IntEnum):
    LOW      = 0
    NORMAL   = 1
    HIGH     = 2
    CRITICAL = 3

class EventBus:
    """
    EventBus is an in-memory publish/subscribe bus with 4 priority levels.
    Handlers are dispatched in CRITICAL-first order.
    """
    def __init__(self):
        import concurrent.futures
        import threading
        self._handlers = {}  # event_type -> list of (priority, handler)
        self._lock = threading.Lock()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="EventBusExecutor")
        self._sequence = 0

    def _next_sequence(self) -> int:
        with self._lock:
            self._sequence += 1
            return self._sequence

    def subscribe(self, event_type, handler, priority=EventPriority.NORMAL):
        with self._lock:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append((priority, handler))
            self._handlers[event_type].sort(key=lambda x: -x[0])

    def publish(self, event_type, payload=None, priority=EventPriority.NORMAL):
        """Default publication. Currently delegates to publish_sync."""
        return self.publish_sync(event_type, payload, priority)

    def publish_sync(self, event_type, payload=None, priority=EventPriority.NORMAL):
        """Synchronously dispatches the event in the current thread."""
        seq = self._next_sequence()
        if payload is not None:
            if hasattr(payload, "sequence_number"):
                payload.sequence_number = seq
            elif isinstance(payload, dict):
                payload["sequence_number"] = seq

        with self._lock:
            handlers = list(self._handlers.get(event_type, []))
        for _, handler in handlers:
            handler(event_type, payload)
        return len(handlers)

    def publish_async(self, event_type, payload=None, priority=EventPriority.NORMAL):
        """Asynchronously schedules the dispatch in a background thread."""
        return self._executor.submit(self.publish_sync, event_type, payload, priority)




# Pre-defined typed event names
class CogOSEvents:
    AGENT_SPAWNED        = "AGENT_SPAWNED"
    AGENT_ARCHIVED       = "AGENT_ARCHIVED"
    HYPOTHESIS_CREATED   = "HYPOTHESIS_CREATED"
    EXPERIMENT_COMPLETED = "EXPERIMENT_COMPLETED"
    PEER_REVIEW_PASSED   = "PEER_REVIEW_PASSED"
    PUBLICATION_ACCEPTED = "PUBLICATION_ACCEPTED"
    MEME_PROPAGATED      = "MEME_PROPAGATED"
    SELECTION_SWEEP      = "SELECTION_SWEEP"
    BUDGET_EXHAUSTED     = "BUDGET_EXHAUSTED"       # CRITICAL
    TASK_SKIPPED         = "TASK_SKIPPED"
    RESOURCE_ALLOCATED   = "RESOURCE_ALLOCATED"
    EPOCH_ADVANCED       = "EPOCH_ADVANCED"         # HIGH
    RESOURCE_UPDATED     = "RESOURCE_UPDATED"
