import random
from dataclasses import dataclass
from runtime.economy.types import AgentId
from runtime.science.artifact import KnowledgeArtifact


@dataclass(frozen=True)
class ReviewResult:
    """
    Result of a peer review evaluation.
    Determines impact on artifact confidence and flags contradictions.
    """
    reviewer:            AgentId
    confidence_delta:    float
    credibility:         float
    contradiction_found: bool


class ReputationPeerReviewer:
    """
    Reputation-weighted Peer Reviewer.
    Impact is scaled by reviewer reputation, and contradiction checks are probabilistic.
    """
    def evaluate_artifact(self, reviewer_id: AgentId, reviewer_reputation: float,
                          artifact: KnowledgeArtifact, seed: int = 42) -> ReviewResult:
        """
        Evaluates an artifact.
        Determistic randomization based on reviewer, artifact, and seed.
        """
        rng = random.Random(seed + hash(reviewer_id) + hash(artifact.artifact_id))

        # Probability of contradiction detection scales with reviewer reputation and artifact's flaws
        base_error_prob = 1.0 - artifact.confidence
        detection_prob  = base_error_prob * reviewer_reputation

        contradiction_found = rng.random() < detection_prob

        if contradiction_found:
            # Drop confidence based on reviewer reputation weight
            confidence_delta = -0.15 * reviewer_reputation
        else:
            # Boost confidence based on reviewer reputation weight
            confidence_delta = 0.10 * reviewer_reputation

        return ReviewResult(
            reviewer=reviewer_id,
            confidence_delta=confidence_delta,
            credibility=reviewer_reputation,
            contradiction_found=contradiction_found
        )


class PeerReview:
    """
    Legacy PeerReview structure to support verification loops
    in test_scientific_method.py.
    """
    @staticmethod
    def verify_and_vote(reviewer, experiment, calculation_func) -> tuple[bool, dict]:
        success, value = experiment.run_trial(calculation_func)
        vote = {
            "agent_id": reviewer.identity.agent_id,
            "agree": success
        }
        return success, vote

