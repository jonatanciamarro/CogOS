import time

class CognitiveEdge:
    """
    CognitiveEdge represents a typed, weighted relational link connecting two concept nodes.
    Supported relations: LINEAGE, CAUSAL, SEMANTIC, CONTRADICTION, EVOLUTION, TEMPORAL.
    """
    def __init__(self, source_uri, target_uri, relation_type, weight=1.0):
        self.source = source_uri
        self.target = target_uri
        self.relation = relation_type
        self.weight = weight
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "weight": self.weight,
            "timestamp": self.timestamp
        }
