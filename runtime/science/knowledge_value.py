from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_stage import ArtifactStage


class KnowledgeValueFunction:
    """
    Computes the subjective cognitive and transaction value of a KnowledgeArtifact.
    Formula:
    Value = novelty + applicability + confidence - contradiction_ratio
    """
    def evaluate_value(self, artifact: KnowledgeArtifact) -> float:
        """
        Calculates the float value representation.
        """
        # Applicability multiplier scales with artifact stage maturity
        applicability = 0.0
        stage = artifact.stage

        if stage == ArtifactStage.TECHNOLOGY:
            applicability = 1.00
        elif stage == ArtifactStage.THEORY:
            applicability = 0.75
        elif stage == ArtifactStage.EVIDENCE:
            applicability = 0.50
        elif stage == ArtifactStage.EXPERIMENT:
            applicability = 0.25
        elif stage == ArtifactStage.HYPOTHESIS:
            applicability = 0.10
        elif stage == ArtifactStage.IDEA:
            applicability = 0.05

        score = (
            artifact.novelty + 
            applicability + 
            artifact.confidence - 
            artifact.contradiction_ratio
        )

        return max(0.0, score)
