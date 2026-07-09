class CognitiveTelemetry:
    """
    CognitiveTelemetry is a pure EventBus observer.
    No class needs to import or call it directly — it auto-subscribes to the bus.
    Satisfies TelemetryProtocol implicitly (PEP 544).
    """
    def __init__(self, limit=500):
        self.limit = limit
        self.buffer = []
        self._event_counts = {}

    def record_event(self, agent_id, phase, action, outcome):
        """Legacy direct-call path — preserved for backward compatibility."""
        event = {
            "agent_id": agent_id, "phase": phase,
            "action": action, "outcome": outcome
        }
        self._append(event)
        return event

    def on_event(self, event_type: str, payload) -> None:
        """EventBus subscriber path — called automatically when events are published."""
        self._event_counts[event_type] = self._event_counts.get(event_type, 0) + 1
        self._append({"event_type": event_type, "payload": payload})

    def snapshot(self) -> dict:
        """Returns a summary of observed events — satisfies TelemetryProtocol."""
        return {
            "buffer_size":   len(self.buffer),
            "event_counts":  dict(self._event_counts),
        }

    def attach_to_bus(self, bus, events: list = None):
        """
        Subscribes to every event in the provided list (or all CogOSEvents by default).
        After this call, no external code needs to interact with Telemetry directly.
        """
        from runtime.bus.event_bus import CogOSEvents, EventPriority
        targets = events or [
            CogOSEvents.AGENT_SPAWNED, CogOSEvents.AGENT_ARCHIVED,
            CogOSEvents.HYPOTHESIS_CREATED, CogOSEvents.EXPERIMENT_COMPLETED,
            CogOSEvents.PEER_REVIEW_PASSED, CogOSEvents.PUBLICATION_ACCEPTED,
            CogOSEvents.MEME_PROPAGATED, CogOSEvents.SELECTION_SWEEP,
            CogOSEvents.BUDGET_EXHAUSTED, CogOSEvents.TASK_SKIPPED,
            CogOSEvents.RESOURCE_ALLOCATED, CogOSEvents.EPOCH_ADVANCED,
            CogOSEvents.RESOURCE_UPDATED,
        ]
        for event_type in targets:
            bus.subscribe(event_type, self.on_event, EventPriority.LOW)

    def _append(self, record: dict):
        self.buffer.append(record)
        if len(self.buffer) > self.limit:
            self.buffer.pop(0)

