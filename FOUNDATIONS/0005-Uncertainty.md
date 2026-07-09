# FOUNDATIONS-0005: Uncertainty Representation

## 1. Objective
To specify how uncertainty, ignorance, and conflicting information are formally represented and handled within the Cognitive Systems Engineering (CSE) framework.

---

## 2. The Three Dimensions of Cognitive Uncertainty

Uncertainty in CSE is not modeled as a single probability value, but mapped along three orthogonal dimensions:

1. **Ignorance (Epistemic Void)**: The absolute lack of observations. The system has no signals or data regarding the phenomenon.
2. **Ambiguity (Epistemic Conflict)**: The presence of contradictory signals or evidence. The system has observed the phenomenon, but the data supports conflicting hypotheses.
3. **Stochasticity (Environmental Noise)**: The inherent randomness of the environment. Noise that cannot be resolved through better observation or reasoning.

---

## 3. Mathematical Representation of Belief Intervals

Uncertainty $U$ is expressed as an epistemic interval:

$$U = [P(H)_{\text{min}}, P(H)_{\text{max}}]$$

Where:
* $P(H)_{\text{min}}$ represents the lower bound of support (the sum of all direct validating evidence).
* $P(H)_{\text{max}}$ represents the upper bound of support ($1$ minus the sum of all refuting evidence).

The width of the interval:

$$\Delta = P(H)_{\text{max}} - P(H)_{\text{min}}$$

represents the **Epistemic Gap** (ignorance). 

* A wide interval ($\Delta \approx 1$) indicates **high ignorance** (lack of observations).
* A narrow interval ($\Delta \approx 0$) with intermediate bounds (e.g. $[0.49, 0.51]$) indicates **high ambiguity** (conflicting observations).

---

## 4. Cognitive Action Under Uncertainty

* **High Ignorance ($\Delta > 0.5$)**: The system must prioritize **exploration** and active experimentation over optimization.
* **High Ambiguity (Low $\Delta$, high conflict)**: The system must pause decision-making and trigger the **Conflict Resolution Protocol** to split concepts or re-evaluate assumptions.
