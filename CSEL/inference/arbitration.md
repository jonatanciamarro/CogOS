# CSEL-0003: Epistemic Arbitration Rules

## 1. Objective
To define the mathematical rules and priority equations for resolving contradictions and deciding between competing hypotheses within the reasoning engine.

---

## 2. Dialectical Competition

Contradiction occurs when two active primitives, $H_1$ and $H_2$, make conflicting claims or predictions within the same context:

$$H_1 \text{ Contradicts } H_2$$

The engine resolves the conflict by calculating which hypothesis represents the **Current Best Theory** using a multi-factor score.

---

## 3. The Epistemic Arbitration Score ($S_{\text{arb}}$)

For any competing hypothesis $H$, the engine computes the Arbitration Score:

$$S_{\text{arb}}(H) = w_c \cdot P(H) + w_e \cdot \sum_{i} \left( W_{e, i} \cdot e^{-\lambda_i \cdot t_i} \cdot S_{e, i} \right) + w_t \cdot \Gamma_{\text{obs}} - w_r \cdot \text{Cost}(H)$$

Where:
* $P(H)$ is the current raw confidence score of the hypothesis.
* $W_{e, i}$ is the weight of supporting evidence node $i$, decayed by its age $t_i$ and the decay constant $\lambda_i$.
* $S_{e, i}$ is the support coefficient of the evidence ($+1.0$ for confirmation, $-1.0$ for contradiction).
* $\Gamma_{\text{obs}}$ is the average trust level of the observers that registered the evidence.
* $\text{Cost}(H)$ is the cognitive resource footprint (memory and compute) needed to evaluate the hypothesis.
* $w_c, w_e, w_t, w_r$ are positive coefficient weights.

---

## 4. Arbitration Decisions

The resolver evaluates the difference:

$$\Delta S = S_{\text{arb}}(H_1) - S_{\text{arb}}(H_2)$$

### Case 1: Decisive Dominance ($\Delta S \ge 0.30$)
The higher-scoring hypothesis is stabilized:
* $H_1$ is marked as the `Current Best Theory`.
* $H_2$ is demoted to `Deprecated` or `Archived` status.

### Case 2: Ambiguous Paraconsistency ($\Delta S < 0.30$)
The system cannot resolve the conflict with current observations:
* Both hypotheses are kept in active memory under `Under Review` status.
* The local **Epistemic Pressure** is incremented.
* The system schedules a **Crucial Experiment** specifically designed to generate divergent predictions and break the tie.
