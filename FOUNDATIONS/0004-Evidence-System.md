# FOUNDATIONS-0004: Evidence System

## 1. Objective
To establish a rigorous mathematical and qualitative framework for evaluating empirical evidence and calculating dynamic changes in the confidence scores of cognitive primitives.

---

## 2. Evidence Weight Scale

Not all evidence carries equal weight. We categorize evidence based on its source and validation strength:

| Level | Weight ($W_e$) | Classification | Source / Verification Description |
| :--- | :--- | :--- | :--- |
| **E-0** | $0.00$ | Anecdotal | Uncontrolled observations, unstructured logs, or conversational feedback. |
| **E-1** | $0.25$ | Simulated | Repeatable observations obtained within synthetic, isolated cognitive testing environments. |
| **E-2** | $0.50$ | Controlled | Systematically designed experiments with baseline controls and isolated variables. |
| **E-3** | $0.75$ | Longitudinal | Multi-environment deployments tracked over time under real-world organizational loads. |
| **E-4** | $1.00$ | Mathematical | Formal proofs, logical invariance, or complete analytical verification. |

---

## 3. Confidence Update Mechanics

When new evidence $E$ is introduced to evaluate a hypothesis or primitive $H$, its confidence score $P(H)$ is updated using a Bayesian-inspired adjustment:

$$P(H | E) = P(H) + W_e \cdot (1 - P(H)) \cdot S_e$$

Where:
* $P(H)$ is the current confidence score of the primitive.
* $W_e$ is the weight of the evidence class (from $0.00$ to $1.00$).
* $S_e$ is the support value of the evidence (ranging from $+1.0$ for complete validation to $-1.0$ for complete refutation).

### Refutation Override

If the evidence directly refutes the core predictions of the primitive ($S_e = -1.0$) and the evidence weight is high ($W_e \ge 0.5$), the confidence immediately collapses to zero:

$$P(H | E) = 0.0$$

The primitive must be moved to the `refuted` state and archived.
