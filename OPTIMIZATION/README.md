# OPTIMIZATION-0000: Knowledge Optimization Passes

## 1. Objective
To specify the optimization and cognitive garbage collection passes executed by the compiler over the intermediate representation (KIR) to keep the graph compact, consistent, and efficient.

---

## 2. Cognitive Garbage Collection Levels

To prevent memory overflow and context explosion, the system manages passive knowledge by routing nodes through three distinct levels of decay (never deleting data, to respect lineage preservation):

### Level 1: Dormant Knowledge
* **Trigger**: Primitives, beliefs, or observations that have not been accessed by any active reasoning loop or decision gate for a specified temporal window.
* **Action**: Moved to cold storage. Only the metadata stub and URI mapping remain in active memory.

### Level 2: Archived Knowledge
* **Trigger**: Concepts or theories that have been superseded by evolved versions (`EvolvedFrom` / `Supersedes`).
* **Action**: Excluded from active reasoning, but retained in LKB for lineage tracing and historical audits.

### Level 3: Invalid Knowledge
* **Trigger**: Hypotheses or theories whose confidence score has collapsed to zero due to experimental refutation ($S_e = -1.0$).
* **Action**: Marked with `STATUS: INVALIDATED` and stamped with the invalidating experiment URI. The node is kept as a logical barrier to prevent the system from re-forming the same discredited hypothesis.

---

## 3. Compiler Optimization Passes

The compiler executes three structural optimization passes over the compiled graph:

### Dead Knowledge Elimination (DKE)
* **Logic**: Identifies and prunes orphan concepts that do not support any invariants, have no downstream dependencies, and contain no active observations.
* **Action**: Archives the nodes, removing them from the runtime execution bundle.

### Semantic Compression
* **Logic**: Scans for redundant nodes or fine-grained clusters of concepts that share identical behaviors and contexts, merging them into a single high-level abstraction:
  $$\text{Concept}_A + \text{Concept}_B + \text{Concept}_C \xrightarrow{\text{Compression}} \text{Concept}_X$$
* **Action**: Collapses node groupings to decrease runtime complexity.

### Contradiction Reduction
* **Logic**: Evaluates the graph for logical conflicts:
  $$(A \text{ DependsOn } B) + (B \text{ Contradicts } A)$$
* **Action**: Locates contradiction loops, raises a compile-time warning, and flags the nodes for paraconsistent suspension if the conflict cannot be resolved.
