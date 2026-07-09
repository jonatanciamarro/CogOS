# META-0009: What is Cognition?

## 1. The Question
What is the core function of "cognition" within an artificial systems engineering discipline? Is it symbol computation, or is it active inference and homeostatic regulation?

---

## 2. Competing Theories

### Theory A: Symbolic Computation (Computationalism)
* **Definition**: Cognition is the execution of algorithms and symbolic manipulation over internal representations, transforming input signals into output states.
* **Assumes**: Cognition is input-driven, computational, and representational. The mind is a computer.
* **Predicts**: Enhancing system capability is purely a function of increasing computational capacity, memory buffers, and inference steps.
* **Testable By**: Measuring task logic accuracy as a function of compute allocation.

### Theory B: Active Inference & Homeostasis (Enactive/Friston)
* **Definition**: Cognition is the continuous process of minimizing prediction error (free energy) and maintaining homeostatic equilibrium through active interaction with the environment.
* **Assumes**: Cognition is survival-driven. The system reasons to prevent its own structural and semantic dissolution.
* **Predicts**: Cognitive systems that are not constrained by homeostatic survival pressures (e.g., energy limits, semantic drift costs) will drift and generate hallucinations.
* **Testable By**: Depriving a reasoning loop of memory and compute costs, and monitoring the velocity of semantic drift in its world model.

---

## 3. Evidence Matrix

| Phenomenon / Anomaly | Theory A (Computationalism) | Theory B (Active Inference) |
| :--- | :--- | :--- |
| **Solving structured puzzles** | Strong (symbolic calculations align with logic outputs) | Moderate (solves puzzles as a method to satisfy predictive consistency) |
| **Hallucination and semantic drift** | Poor (struggles to explain why unconstrained generators drift away from target truth) | Strong (drift is the natural state of systems lacking homeostatic pressure) |
| **Autonomous motivation** | Poor (motivation must be externally injected as a hard-coded objective function) | Strong (motivation is the thermodynamic necessity to preserve internal structure) |

---

## 4. Current Best Theory
**Theory B (Active Inference & Homeostasis)** is selected as the current best theory.

* **Justification**: Computationalism has produced powerful generators, but it fails to produce self-governing systems. If CogOS is to act as an autonomous cognitive ecosystem, its operations must be bound by homeostatic rules (semantic integrity, epistemic pressure, resource costs). Cognition in CSE is the engine that acts to preserve the system's structural sanity under time and noise.
