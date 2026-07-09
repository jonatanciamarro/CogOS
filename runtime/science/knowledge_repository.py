class KnowledgeRepository:
    """
    KnowledgeRepository stores peer-reviewed publication indexes and audits
    node transitions (Hypothesis -> Theory -> Law).
    Extended to store and query KnowledgeArtifact instances.
    """
    def __init__(self, graph_knowledge_engine=None):
        self.graph = graph_knowledge_engine
        self.publications = {}  # paper_id -> ScientificPaper
        self.artifacts = {}     # artifact_id -> KnowledgeArtifact

    def register_artifact(self, artifact) -> None:
        """Stores a KnowledgeArtifact in the repository."""
        self.artifacts[artifact.artifact_id] = artifact

    def get_artifact(self, artifact_id: str):
        """Retrieves a KnowledgeArtifact by ID."""
        return self.artifacts.get(artifact_id)

    def get_all_artifacts(self) -> list:
        """Returns all stored KnowledgeArtifacts."""
        return list(self.artifacts.values())

    def get_by_stage(self, stage) -> list:
        """Returns all stored KnowledgeArtifacts at a given stage."""
        return [art for art in self.artifacts.values() if art.stage == stage]

    def register_publication(self, paper):
        self.publications[paper.id] = paper

    def audit_concept_maturity(self, concept_node_id, replication_count, contradiction_ratio=0.00):
        """
        Promotes concepts based on replication counts and contradiction weights.
        - Theory requires >=3 replications.
        - Law requires >=10 replications and <0.05 (5%) contradiction ratio.
        """
        if not self.graph:
            return "UNKNOWN"
        node = self.graph.get_node(concept_node_id)
        if not node:
            return "UNKNOWN"

        if replication_count >= 10 and contradiction_ratio < 0.05:
            node.node_type = "Law"
            return "LAW"
        elif replication_count >= 3:
            node.node_type = "Theory"
            return "THEORY"
        
        node.node_type = "Hypothesis"
        return "HYPOTHESIS"
