from runtime.memory.node import CognitiveNode
from runtime.memory.edge import CognitiveEdge

class GraphKnowledgeEngine:
    """
    GraphKnowledgeEngine manages the directed property graph database of the LKB,
    supporting typed vertices, directed edges, and graph metrics tracking.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, concept, node_type, confidence=1.0, entropy=0.0, lineage_id=None):
        """
        Creates and stores a CognitiveNode in the graph registry.
        """
        node = CognitiveNode(node_id, concept, node_type, confidence, entropy, lineage_id)
        self.nodes[node_id] = node
        return node

    def add_relationship(self, source_uri, target_uri, relation_type, weight=1.0):
        """
        Creates and appends a CognitiveEdge between two nodes.
        """
        edge = CognitiveEdge(source_uri, target_uri, relation_type, weight)
        self.edges.append(edge)
        return edge

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def get_edges_for_node(self, node_id):
        """
        Queries all incoming/outgoing edges relative to the node ID.
        """
        return [edge for edge in self.edges if edge.source == node_id or edge.target == node_id]

    def update_state_metadata(self, state):
        """
        Updates the target CVM state structure with graph density and counts.
        """
        state.memory_metadata["node_count"] = len(self.nodes)
        state.memory_metadata["relationship_count"] = len(self.edges)
        
        # Calculate simple topology hash
        state.memory_metadata["graph_hash"] = hash(tuple(sorted(self.nodes.keys())))
