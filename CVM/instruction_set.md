# CVM-0004: Cognitive Instruction Set Architecture (ISA)

## 1. Objective
To define the formal instruction set of the CVM, detailing the input, output, execution cost, and state transition semantics of each operational opcode.

---

## 2. Sensory Instructions

* **`OBSERVE %reg_dest, [Signal_URI]`**:
  * **Semantics**: Reads `cse://signal/` and synthesizes it with the context in `CR0` to create an `Observation` in `reg_dest`.
  * **Cost**: Low memory, low compute.
  * **State Transition**: $\Omega \to \Omega + \text{Obs}$.
* **`CAPTURE_SIGNAL %reg_dest, [Sensor_ID]`**:
  * **Semantics**: Captures raw hardware/API outputs from `Sensor_ID`, emitting a signal node.
* **`CREATE_CONTEXT %reg_dest, [Parameter_List]`**:
  * **Semantics**: Writes context boundaries and noise limits into the target register or `CR0`.

---

## 3. Memory Instructions

* **`STORE %reg_src, [Memory_Class]`**:
  * **Semantics**: Persists register contents into target memory partition (*Working*, *Semantic*, *Episodic*, or *Genetic*).
* **`RECALL %reg_dest, [Memory_URI]`**:
  * **Semantics**: Loads a node from Memory into registers.
* **`FORGET %reg_src`**:
  * **Semantics**: Demotes a node from Working Memory to cold storage or marks it as deprecated. Triggers an `Evolution Value` calculation to satisfy the conservation equation.
* **`ARCHIVE %reg_src`**:
  * **Semantics**: Moves a node to Genetic Memory, freezing its state for historical audit.

---

## 4. Reasoning Instructions

* **`INFER %reg_dest, %reg_src, [Inference_Mode]`**:
  * **Semantics**: Executes Deduction, Induction, or Abduction over `reg_src`.
  * **Cost**: High compute, moderate memory.
* **`ANALOGIZE %reg_dest, %reg_domain_A, %reg_domain_B`**:
  * **Semantics**: Maps relational schemas between two separate conceptual domains.
* **`PREDICT %reg_dest, %reg_model, %reg_context`**:
  * **Semantics**: Generates expected future signals based on active theories.

---

## 5. Epistemic Instructions

* **`VERIFY %reg_dest, %reg_belief, %reg_evidence`**:
  * **Semantics**: Evaluates the belief interval of the target, writing support and confidence deltas.
  * **State Transition**: Updates `CR4` (Uncertainty) and $P(H)$ parameters.
* **`RESOLVE_CONTRADICTION %reg_dest, %reg_H1, %reg_H2`**:
  * **Semantics**: Resolves conflict between two contradicting hypotheses using the Epistemic Arbitration Score ($S_{\text{arb}}$).
* **`COLLAPSE_DECISION %reg_dest, %reg_knowledge, %reg_purpose`**:
  * **Semantics**: Executes a gate action selection. Writes the candidate decision to `CR3`.

---

## 6. Evolution Instructions

* **`MUTATE_MODEL %reg_dest, %reg_model, %reg_feedback`**:
  * **Semantics**: Reorganizes ontology structures based on verification anomalies.
* **`SPLIT_CONCEPT %reg_dest, %reg_source`**:
  * **Semantics**: Divides an ambiguous concept into separate context-specific nodes.
* **`MERGE_CONCEPT %reg_dest, %reg_A, %reg_B`**:
  * **Semantics**: Combines redundant nodes, updating dependencies.
