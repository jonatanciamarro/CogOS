import time
import hashlib
import uuid

class AgentEvent:
    """
    AgentEvent represents a single immutable transaction block inside the event ledger.
    """
    def __init__(self, event_type, agent_id, payload, previous_hash="0"):
        self.event_id = str(uuid.uuid4())
        self.agent_id = agent_id
        self.timestamp = time.time()
        self.event_type = event_type
        self.payload = payload
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw_str = f"{self.agent_id}-{self.timestamp}-{self.event_type}-{self.payload}-{self.previous_hash}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()


class AgentEventLog:
    """
    AgentEventLog coordinates an append-only transaction registry with integrity audits.
    """
    def __init__(self):
        self.ledger = []

    def append(self, event_type, agent_id, payload):
        """
        Appends a new event block, binding it cryptographically to the predecessor.
        """
        previous_hash = self.ledger[-1].hash if self.ledger else "0"
        event = AgentEvent(event_type, agent_id, payload, previous_hash)
        self.ledger.append(event)
        return event

    def verify_integrity(self):
        """
        Verifies that no ledger records have been tampered with or modified.
        """
        for i, current in enumerate(self.ledger):
            if current.hash != current.calculate_hash():
                return False
            if i > 0:
                previous = self.ledger[i - 1]
                if current.previous_hash != previous.hash:
                    return False
        return True
