# FOUNDATIONS-0002: Falsifiability Criteria

## 1. Objective
To prevent philosophical bloat and dogmatism by establishing clear rules under which any Cognitive Primitive or Hypothesis can be proven wrong.

---

## 2. The Popperian Boundary

For any concept, hypothesis, or primitive to be integrated into the CogOS Reference Architecture, it must make assertions that are falsifiable. 

* **Falsifiable Claim**: A statement that defines a specific state of affairs that, if observed, would prove the statement incorrect.
* **Unfalsifiable Claim**: A statement that can explain any possible observation, leaving no room for refutation.

---

## 3. The Refutation Checklist

Every Cognitive Primitive must explicitly outline its failure modes and counterexamples. The **Meta-Scientist** evaluates each primitive against the following rules:

1. **Predictive Specificity**: Does the primitive state a prediction (`PREDICTS`) that can be quantitatively or qualitatively measured in a simulation or deployment?
2. **Refutation Protocol**: Does it specify exactly what observation or experimental outcome would invalidate it (`INVALIDATES`)?
3. **No Retroactive Immunization**: If an experiment fails to validate the prediction, the primitive cannot be retroactively modified to fit the data without decreasing its confidence and restarting the review loop.

---

## 4. Confidence Score Mechanics

Every primitive has a `CONFIDENCE` score between $0.0$ and $1.0$:

* **$0.0 - 0.2$ (Speculative / Hypothesis)**: Conceptually defined, but lacks empirical support or tests.
* **$0.3 - 0.6$ (Active Testing)**: The primitive is undergoing simulation or empirical testing. Some evidence exists.
* **$0.7 - 0.9$ (Verified Theory)**: Supported by multiple distinct experiments with no observed counterexamples.
* **$1.0$ (Epistemic Invariant)**: Axiomatic, logically absolute, or mathematically proven within the system boundary.

> [!WARNING]
> A single verified counterexample or test failure immediately triggers an automated reduction in the confidence score and forces the primitive into `Under Review` or `Deprecated` status.
