from runtime.science.artifact import KnowledgeArtifact
from runtime.science.artifact_stage import ArtifactStage


def promote_artifact(artifact: KnowledgeArtifact) -> KnowledgeArtifact:
    """
    Evaluates transitions in the maturity state machine of the artifact.
    Must be a pure function.
    
    Transition rules:
    - IDEA -> HYPOTHESIS: confidence > 0.6
    - HYPOTHESIS -> EXPERIMENT: replications >= 1
    - EXPERIMENT -> EVIDENCE: replications >= 2 and contradiction_ratio < 0.20
    - EVIDENCE -> THEORY: replications >= 3 and contradiction_ratio < 0.10
    - THEORY -> TECHNOLOGY: replications >= 10 and contradiction_ratio < 0.05
    """
    current_stage = artifact.stage
    next_stage = current_stage

    if current_stage == ArtifactStage.IDEA:
        if artifact.confidence > 0.6:
            next_stage = ArtifactStage.HYPOTHESIS
    elif current_stage == ArtifactStage.HYPOTHESIS:
        if artifact.replications >= 1:
            next_stage = ArtifactStage.EXPERIMENT
    elif current_stage == ArtifactStage.EXPERIMENT:
        if artifact.replications >= 2 and artifact.contradiction_ratio < 0.20:
            next_stage = ArtifactStage.EVIDENCE
    elif current_stage == ArtifactStage.EVIDENCE:
        if artifact.replications >= 3 and artifact.contradiction_ratio < 0.10:
            next_stage = ArtifactStage.THEORY
    elif current_stage == ArtifactStage.THEORY:
        if artifact.replications >= 10 and artifact.contradiction_ratio < 0.05:
            next_stage = ArtifactStage.TECHNOLOGY

    if next_stage == current_stage:
        return artifact

    return KnowledgeArtifact(
        artifact_id=artifact.artifact_id,
        title=artifact.title,
        stage=next_stage,
        confidence=artifact.confidence,
        replications=artifact.replications,
        contradictions=artifact.contradictions,
        novelty=artifact.novelty,
        author=artifact.author,
        parent_artifact_id=artifact.parent_artifact_id,
        contributors=artifact.contributors,
        created_tick=artifact.created_tick,
        accessibility=artifact.accessibility
    )


def replicate_artifact(artifact: KnowledgeArtifact, success: bool) -> KnowledgeArtifact:
    """
    Conducts a replication trial on the artifact.
    Increments replications or contradictions and shifts confidence.
    Must be a pure function.
    """
    conf_change = 0.05 if success else -0.10
    new_confidence = max(0.0, min(1.0, artifact.confidence + conf_change))
    new_reps = artifact.replications + (1 if success else 0)
    new_contra = artifact.contradictions + (0 if success else 1)

    return KnowledgeArtifact(
        artifact_id=artifact.artifact_id,
        title=artifact.title,
        stage=artifact.stage,
        confidence=new_confidence,
        replications=new_reps,
        contradictions=new_contra,
        novelty=artifact.novelty,
        author=artifact.author,
        parent_artifact_id=artifact.parent_artifact_id,
        contributors=artifact.contributors,
        created_tick=artifact.created_tick,
        accessibility=artifact.accessibility
    )


def review_artifact(artifact: KnowledgeArtifact, confidence_delta: float) -> KnowledgeArtifact:
    """
    Applies peer-review evaluations to adjust artifact confidence.
    Must be a pure function.
    """
    new_confidence = max(0.0, min(1.0, artifact.confidence + confidence_delta))
    return KnowledgeArtifact(
        artifact_id=artifact.artifact_id,
        title=artifact.title,
        stage=artifact.stage,
        confidence=new_confidence,
        replications=artifact.replications,
        contradictions=artifact.contradictions,
        novelty=artifact.novelty,
        author=artifact.author,
        parent_artifact_id=artifact.parent_artifact_id,
        contributors=artifact.contributors,
        created_tick=artifact.created_tick,
        accessibility=artifact.accessibility
    )
