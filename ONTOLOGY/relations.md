# ONTOLOGY-0000: Relationship Semantics

## 1. Objective
To define the formal relational vocabulary of the Cognitive Systems Engineering Reference Standard (CSERS). Every edge in the compiled Knowledge Graph must correspond to one of these types.

---

## 2. Structural & Epistemic Relations

### DependsOn
* **Signature**: $A \text{ DependsOn } B$ where $A, B \in \text{COM}$
* **Algebraic Rule**: If $P(B) \to 0$ (refuted), then $P(A) \to 0$ (logical decay).

### Contradicts
* **Signature**: $A \text{ Contradicts } B$ where $A, B \in \text{COM}$
* **Algebraic Rule**: Asserting both $A$ and $B$ simultaneously triggers an increase in Epistemic Pressure:
  $$\Delta P_{ep} \propto P(H_A) \cdot P(H_B)$$

### Refines
* **Signature**: $A \text{ Refines } B$ where $A, B \in \text{COM}$
* **Algebraic Rule**: $A$ inherits the constraints of $B$ and adds specific context parameters.

### Generalizes
* **Signature**: $A \text{ Generalizes } B$ where $A, B \in \text{COM}$
* **Algebraic Rule**: Inverse of *Refines*. $A$ acts as a parent abstraction class of $B$.

### Implements
* **Signature**: $A \text{ Implements } B$ where $A \in \text{Runtime Entity / Capability}$ and $B \in \text{Standard Protocol / Concept}$

### Observes
* **Signature**: $A \text{ Observes } B$ where $A \in \text{Observer}$ and $B \in \text{Signal}$

### Measures
* **Signature**: $A \text{ Measures } B$ where $A \in \text{Metric / Benchmark}$ and $B \in \text{Capability / State}$

### Tests
* **Signature**: $A \text{ Tests } B$ where $A \in \text{Experiment}$ and $B \in \text{Hypothesis / Theory}$

### Explains
* **Signature**: $A \text{ Explains } B$ where $A \in \text{Theory / Proof}$ and $B \in \text{Anomaly / Observation}$

### Predicts
* **Signature**: $A \text{ Predicts } B$ where $A \in \text{Primitive}$ and $B \in \text{Expected Signal / Event}$

---

## 3. Temporal & Evolutionary Relations

### EvolvedFrom
* **Signature**: $A \text{ EvolvedFrom } B$ where $A \in \text{Concept } v_{t1}$ and $B \in \text{Concept } v_{t0}$
* **Algebraic Rule**: Preserves lineage history across updates.

### Supersedes
* **Signature**: $A \text{ Supersedes } B$ where $A, B \in \text{COM}$
* **Algebraic Rule**: $A$ replaces $B$ in active memory. $B$ is flagged as `Archived` or `Invalid`.

### CreatedBy
* **Signature**: $A \text{ CreatedBy } B$ where $A \in \text{COM}$ and $B \in \text{Cognitive Actor / Process}$

### ObservedAt
* **Signature**: $A \text{ ObservedAt } t$ where $A \in \text{Signal / Event}$ and $t \in \text{SystemTime}$

### ValidUntil
* **Signature**: $A \text{ ValidUntil } t$ where $A \in \text{Context / Knowledge}$ and $t \in \text{SystemTime}$
* **Algebraic Rule**: When $t_{\text{current}} > t$, triggers automatic decay and reversion to the `UNOBSERVED` negative space.

### ChangedAfter
* **Signature**: $A \text{ ChangedAfter } t$ where $A \in \text{State}$ and $t \in \text{SystemTime}$

### TriggeredBy
* **Signature**: $A \text{ TriggeredBy } B$ where $A \in \text{Event / Transformation}$ and $B \in \text{Signal / Event}$
