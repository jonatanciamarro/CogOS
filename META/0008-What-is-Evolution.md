# META-0008: What is Evolution?

## 1. The Question
How does evolution operate within a cognitive ecosystem? What are the mechanisms of variation, inheritance, and selection of cognitive structures?

---

## 2. Competing Theories

### Theory A: Parameter-Space Selection (Darwinian Optimization)
* **Definition**: Evolution is the generation of random numerical changes in a fixed coordinate space, followed by selection of the fittest parameter sets based on an external fitness evaluation.
* **Assumes**: The structure of the genome (the code template or model architecture) is fixed. Only values mutate.
* **Predicts**: Optimization is slow, non-directed, and requires massive populations of trial variants.
* **Testable By**: Running genetic algorithms over model parameters and tracking convergence speed.

### Theory B: Ontological Lineage & Mutation (Lamarckian Adaptation)
* **Definition**: Evolution is the structural refactoring, lineage tracking, and heritage transmission of cognitive genomes (ontologies, invariants, and policies) driven by the need to survive model updates and environmental shifts.
* **Assumes**: The genome structure itself is dynamic and self-directing. Acquired knowledge can be written back into the genome (Lamarckian inheritance).
* **Predicts**: Cognitive structures can survive the complete replacement of their underlying processing models (e.g., swapping LLMs) because their inherited ontology is model-agnostic.
* **Testable By**: Upgrading the execution models of a system and measuring how much of the acquired operational ontology persists.

---

## 3. Evidence Matrix

| Phenomenon / Anomaly | Theory A (Parameters) | Theory B (Ontology) |
| :--- | :--- | :--- |
| **Numeric weight optimization** | Strong (highly effective at fine-tuning local functions) | Poor (struggles to represent raw floating-point adjustments) |
| **Model migration (LLM upgrades)** | Poor (trained parameters are completely lost when swapping models) | Strong (structural rules and context files are independent and survive) |
| **Inherited experience integration** | Poor (requires retraining weights to include new facts) | Strong (direct editing of cognitive primitives allows instant heritage updates) |

---

## 4. Current Best Theory
**Theory B (Ontological Lineage & Mutation)** is selected as the current best theory.

* **Justification**: CogOS cannot treat learning as a disposable commodity tied to a single model's weights. If we upgrade from Gemini 1.5 to Gemini 2.0, the system must inherit its entire history of observations, corrections, and structure. We require a system of evolution that operates on the symbolic, ontologic genome, enabling Lamarckian learning where the ecosystem directly preserves and passes down its acquired wisdom.
