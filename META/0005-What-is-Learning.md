# META-0005: What is Learning?

## 1. The Question
How does learning occur within a cognitive ecosystem, and what structures are modified during the process?

---

## 2. Competing Theories

### Theory A: Parameter Adjustment (Statistical Optimization)
* **Definition**: Learning is the mathematical tuning of weights, parameters, or coefficients within a fixed functional structure to minimize prediction error.
* **Assumes**: The system's architecture and vocabulary are static. Learning is quantitative interpolation.
* **Predicts**: Learning is gradual, requiring large volumes of data and repeated training epochs.
* **Testable By**: Monitoring loss functions and accuracy charts during model training.

### Theory B: Epistemic Reorganization (Structural Refactoring)
* **Definition**: Learning is the qualitative refactoring of the system's world model, involving the creation, division, merger, or deprecation of cognitive primitives and relations to resolve anomalies.
* **Assumes**: Learning is structural. It is driven by epistemic pressure when current models fail to explain observed phenomena.
* **Predicts**: The system can execute rapid, "one-shot" conceptual adaptations by modifying its ontological graph.
* **Testable By**: Presenting a node with a single extreme predictive failure and measuring if it automatically splits an existing primitive to accommodate the anomaly.

---

## 3. Evidence Matrix

| Phenomenon / Anomaly | Theory A (Parameters) | Theory B (Reorganization) |
| :--- | :--- | :--- |
| **Statistical pattern recognition** | Strong (high efficiency in static environments) | Moderate (requires compiling raw data patterns into symbolic primitives) |
| **One-Shot conceptual shifts** | Poor (requires fine-tuning over large datasets) | Strong (restructures the relationships of primitives instantly) |
| **Auditability and safety** | Poor (opaque, distributed parameter weights) | Strong (discrete, inspectable primitives with lineage logging) |

---

## 4. Current Best Theory
**Theory B (Epistemic Reorganization)** is selected as the current best theory.

* **Justification**: A cognitive operating system must be auditable and capable of rapid adaptation. If learning is merely weight adjustment, the system's knowledge is locked in a black box. Epistemic Reorganization treats learning as the evolution of the repository's ontology—allowing the system to learn new rules, deprecate refuted beliefs, and explain *why* it changed its behavior.
