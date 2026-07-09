class CognitiveStateInspector:
    """
    CognitiveStateInspector provides query methods to inspect and audit internal parameters.
    """
    @staticmethod
    def inspect_graph_density(context):
        metadata = context.state.memory_metadata
        density = 0.0
        if metadata["node_count"] > 0:
            density = metadata["relationship_count"] / metadata["node_count"]
        return {
            "density": density,
            "node_count": metadata["node_count"],
            "relationship_count": metadata["relationship_count"]
        }
