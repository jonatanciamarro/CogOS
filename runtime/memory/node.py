import time

class CognitiveNode:
    """
    CognitiveNode represents a unique concept vertex in the Knowledge Graph database.
    """
    def __init__(self, node_id, concept, node_type, confidence=1.0, entropy=0.0, lineage_id=None):
        self.id = node_id
        self.concept = concept
        self.type = node_type
        self.confidence = confidence
        self.entropy = entropy
        self.lineage_id = lineage_id
        self.created_at = time.time()

    def to_dict(self):
        return {
            "id": self.id,
            "concept": self.concept,
            "type": self.type,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "lineage_id": self.lineage_id,
            "created_at": self.created_at
        }
