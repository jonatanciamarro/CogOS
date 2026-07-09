import uuid
import time
import hashlib

class AgentIdentity:
    """
    AgentIdentity represents the immutable DNA and lineage metadata of a Cognitive Agent.
    Once initialized, its parameters are read-only to preserve security invariants.
    """
    def __init__(self, parent_id=None, creation_reason="genesis", constitution_hash="base_hash"):
        self._agent_id = str(uuid.uuid4())
        self._parent_id = parent_id
        self._lineage_root = parent_id if parent_id else self._agent_id
        self._created_at = time.time()
        self._creation_reason = creation_reason
        self._constitution_hash = constitution_hash

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def lineage_root(self):
        return self._lineage_root

    @property
    def created_at(self):
        return self._created_at

    @property
    def creation_reason(self):
        return self._creation_reason

    @property
    def constitution_hash(self):
        return self._constitution_hash

    def calculate_checksum(self):
        """
        Computes a cryptographic signature of the immutable parameters.
        """
        raw_str = f"{self._agent_id}-{self._parent_id}-{self._lineage_root}-{self._created_at}-{self._constitution_hash}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
