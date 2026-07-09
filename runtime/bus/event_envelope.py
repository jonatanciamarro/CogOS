from dataclasses import dataclass, field
from runtime.bus.event_bus import EventPriority
import uuid, time


@dataclass
class EventEnvelope:
    """
    EventEnvelope wraps every event on the CogOS bus.
    Prepares for distributed tracing without breaking existing local usage.
    """
    event_type:   str
    payload:      dict
    priority:     EventPriority = EventPriority.NORMAL
    id:           str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp:    float = field(default_factory=time.monotonic)
    origin:       str = ""          # agent_id or system name that emitted this
    trace_id:     str = ""          # root trace chain identifier
    parent_event: str = ""          # id of the event that triggered this one
    sequence_number: int = 0        # execution ordering assigned by the EventBus

