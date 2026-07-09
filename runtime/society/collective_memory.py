class CollectiveMemory:
    """
    CollectiveMemory manages public knowledge spaces, writing concepts committed via consensus.
    """
    def __init__(self, graph_knowledge_engine):
        self.graph = graph_knowledge_engine
        self.committed_proposals = {}  # concept_id -> consensus_score

    def propose_and_commit(self, concept_id, concept_data, consensus_score):
        """
        Commits concept node to the Graph Knowledge base if consensus score passes 0.70 threshold.
        """
        if consensus_score >= 0.70:
            self.graph.add_node(
                concept_id, 
                concept_data.get("concept", "shared_concept"), 
                concept_data.get("type", "SharedConcept"),
                confidence=consensus_score,
                lineage_id=concept_data.get("lineage_id")
            )
            self.committed_proposals[concept_id] = consensus_score
            return True
            
        return False
