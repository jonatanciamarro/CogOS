# COM-0001: Cognitive Type System (CTS)

## 1. Objective
To define the formal types and meta-types of the Cognitive Systems Engineering Reference Standard (CSERS), establishing constraints on how entities represent structures and dynamic processes.

---

## 2. Core Cognitive Types

These types represent the structural and epistemic entities within the Living Knowledge Base (LKB):

* **Primitive**: The root type from which all other cognitive objects inherit.
* **Concept**: A defined representation summarizing a pattern, entity class, or relationship.
* **Abstract Concept**: Concept interfaces that cannot be directly instantiated (e.g., *cse://concept/meaning*).
* **Operational Concept**: Realized concepts that map directly to runtime structures or functions.
* **Protocol**: Semantic contracts governing transitions of state between layers.
* **Capability**: Functional descriptions of what the system can execute (inputs, outputs, and limits).
* **Law**: A universally consistent, invariant relation supported by level E-4 evidence.
* **Theory**: A candidate framework supported by active evidence and testable predictions.
* **Evidence**: Grounded signals validated by a trusted observer verifying or refuting a prediction.
* **Signal**: Raw environmental or computational inputs registered by a sensor.
* **Question**: Active research nodes compiling competing theories and evidence.
* **Experiment**: Test protocols defining validation steps for hypotheses.

---

## 3. Cognitive Meta-Types (System Dynamics)

To model time, observation, and state mutations, the CTS incorporates eight dynamic meta-types:

* **Observer**: An active cognitive frame of reference that draws distinctions and interprets signals.
* **Context**: The environmental conditions, constraints, and histories that frame an observation.
* **Constraint**: An ontological parameter that must be satisfied for a concept to remain valid.
* **Invariant**: Constitution-level axioms that cannot be violated by any compiler optimization or runtime execution.
* **Transformation**: An algebraic transition mapping inputs to outputs (e.g., $A \xrightarrow{f} B$).
* **Process**: A coordinated sequence of cognitive transformations executed over time.
* **State**: The snapshot of beliefs, resource levels, and active concepts at a specific timestamp $t$.
* **Event**: A discrete signal triggering a transformation or transition in state.
