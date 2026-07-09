from enum import Enum

class AgentLifecycleState(Enum):
    """
    AgentLifecycleState defines the operational lifecycle modes of a Cognitive Agent.
    """
    CREATED = 1
    BOOTING = 2
    ACTIVE = 3
    SUSPENDED = 4
    ARCHIVED = 5
    QUARANTINED = 6
