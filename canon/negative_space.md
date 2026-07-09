# canon-negative-space: The Taxonomy of the Unknown

## 1. Objective
To establish a formal classification system for representing and managing the boundaries of system knowledge, ensuring the ecosystem actively tracks its own ignorance, contradictions, and limits.

---

## 2. The Negative Space Classification

We divide the negative space of CogOS into five distinct zones:

### 1. UNKNOWN
* **Definition**: Conceptual domains or phenomena that have not yet been modeled. The system contains no primitives or vocabulary to represent these zones.
* **System Action**: Identified as "epistemic void". Flagged for high-level research. The system must not make decisions dependent on this domain.

### 2. UNOBSERVED
* **Definition**: Cognitive primitives or hypotheses that are conceptually defined but lack any empirical signals or data records in the Observatory.
* **System Action**: System schedules sensing protocols to search for environmental signals matching the primitive's definition.

### 3. UNPROVEN
* **Definition**: Primitives or theories that possess observations but lack formal proofs, verified predictions, or experimental validation ($\text{Confidence} < 0.30$).
* **System Action**: Queued in the Experiments engine for verification.

### 4. CONTRADICTED
* **Definition**: Primitives that are active but have triggered verified counterexamples, or whose predictions directly conflict with other validated primitives.
* **System Action**: Triggers a spike in **Epistemic Pressure**. The system halts dependent processes and initiates the **Conflict Resolution Protocol**.

### 5. IMPOSSIBLE
* **Definition**: States, transformations, or actions that directly violate the foundational invariants of the system (e.g., trying to generate meaning without an observer).
* **System Action**: Actively blocked by compile-time or runtime checks. Primitives matching this definition are permanently deprecated.
