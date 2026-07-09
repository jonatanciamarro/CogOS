# CVM-KERN-0000: Cognitive Syscalls

## 1. Objective
To define the formal system calls (syscalls) that enable compiled CSEL programs to interact safely with CVM hardware subsystems and graph memory partitions without direct, unmonitored write access.

---

## 2. Standard Syscall Interface

Compliant runtimes must implement five standard syscall vectors:

### 1. `SYS_OBSERVE(Signal_URI, Context_URI) -> Observation_URI`
* **Objective**: Instructs the kernel to ingest a signal, verify its context limits against active variables, and emit an observation node.
* **Kernel Rule**: Verifies that the observing actor has valid credentials registered in `CR0`.

### 2. `SYS_COMMIT_KNOWLEDGE(Belief_URI, Evidence_URI) -> Knowledge_URI`
* **Objective**: Requests the promotion of an active belief to stabilized knowledge (Epistemic Collapse).
* **Kernel Rule**: Verifies that the supporting evidence node weight $W_e \ge 0.50$, and enforces CSA lineage logging (writing the output to `CR6`).

### 3. `SYS_REVISE_MODEL(Model_URI, Anomaly_Evidence_URI) -> MutationReceipt`
* **Objective**: Initiates an ontological mutation (Split or Merge) of target concept nodes in Semantic Memory.
* **Kernel Rule**: Validates that the mutation result complies with the Cognitive Conservation Equation ($\Delta L + \Delta K + \Delta U + \Delta C + \Delta E_v \ge 0$).

### 4. `SYS_ALLOCATE_ATTENTION(Target_Process_ID, Budget) -> Status`
* **Objective**: Adjusts the priority and attention allocation (`CR7`) of the target thread.
* **Kernel Rule**: Verifies that the calling process possesses sufficient remaining resources in its `CR5` budget.

### 5. `SYS_ARCHIVE_MEMORY(Node_URI) -> LineageStub_URI`
* **Objective**: Demotes a concept or belief from active Semantic Memory to Genetic Memory.
* **Kernel Rule**: Enforces that active references to the archived node are preserved by generating lineage stubs.
