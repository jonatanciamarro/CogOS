# FOUNDATIONS-0007: Conflict Resolution Protocol

## 1. Objective
To specify how competing hypotheses or contradictory primitives are resolved within the ecosystem when epistemic pressure peaks.

---

## 2. Epistemic Pressure Mechanics

**Epistemic Pressure ($P_{ep}$)** is a system-wide or domain-specific metric representing the level of unresolved conflict or contradiction within the cognitive ecosystem. It is formulated as:

$$P_{ep} = \sum_{i} \Omega_i \cdot \mathcal{C}(H_{i1}, H_{i2})$$

Where:
* $\Omega_i$ is the systemic weight or operational importance of domain $i$.
* $\mathcal{C}(H_{i1}, H_{i2})$ is the semantic divergence or contradiction level between competing active hypotheses $H_1$ and $H_2$.

High epistemic pressure causes systemic instability, causing the Meta-Scientist or the cognitive schedulers to allocate resources to resolution.

---

## 3. Resolution Escalation Paths

When two active hypotheses contradict each other, the system executes three progressive escalation steps:

### Phase 1: Crucial Experimentation
The system designs a **Crucial Experiment**—a protocol specifically structured to produce divergent outcomes for $H_1$ and $H_2$.
* If the result aligns with $H_1$ and invalidates $H_2$'s predictions: $P(H_1)$ increases, and $P(H_2) \to 0$.

### Phase 2: Contextual Splitting (Epistemic Refinement)
If experiments show that $H_1$ is true under condition $X$ and $H_2$ is true under condition $Y$:
* The system refines the ontology by defining separate scopes.
* The original primitive is split:
  $$\text{Primitive}_H \xrightarrow{\text{Split}} H_1(\text{Context: } X) + H_2(\text{Context: } Y)$$

### Phase 3: Paraconsistent Suspension
If no experimental resolution is currently possible due to system constraints:
* The system flags the domain as `Ambiguous` within the Cânone.
* Confidence scores for both are capped at $0.4$.
* All downstream automated decisions dependent on these primitives are suspended until the ambiguity is reduced.
