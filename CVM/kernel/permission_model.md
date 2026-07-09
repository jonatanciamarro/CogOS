# CVM-KERN-0002: Cognitive Permission Model

## 1. Objective
To define the security policies, access control lists, and permission scopes that govern how cognitive processes and threads interact with the shared Knowledge Graph memory partitions.

---

## 2. Epistemic Permission Levels

Access to the LKB is governed by three hierarchical permission levels:

| Permission Level | Access Scope | Allowed Operations / Opcodes | Target Memory Partitions |
| :--- | :--- | :--- | :--- |
| **`E-READ`** | Read-Only | `RECALL` | Semantic, Episodic, Genetic Memory |
| **`E-WRITE`** | Grounded Read/Write | `SYS_OBSERVE`, `SYS_COMMIT_KNOWLEDGE`, `STORE` | Working Memory, Episodic Memory |
| **`E-EVOLVE`** | Ontological Mutation | `SYS_REVISE_MODEL`, `SPLIT_CONCEPT`, `MERGE_CONCEPT` | Semantic Memory, Genetic Memory |

---

## 3. Partition Boundary Rules

* **Working Memory Isolation**: A thread possesses exclusive read/write access to its local register set (`CR0` to `CR8`). It is mathematically blocked from reading or writing the registers of concurrent threads.
* **Semantic Memory Protection**: Standard application threads are restricted to `E-READ` access. Only kernel-level optimization routines or governance threads possessing verified `E-EVOLVE` keys may execute structural mutations.
* **Genetic Memory Inviolability**: This partition is permanently read-only for all external processes. Only the kernel itself may append nodes to Genetic Memory during archival or deprecation cycles.

---

## 4. Verification & Violation Handling

During the **Validate** stage of the instruction execution cycle:
1. The CVM decodes the target operation.
2. It verifies the thread's permission level against the target memory partition.
3. If an `E-WRITE` thread attempts to call an evolution instruction (such as `SYS_REVISE_MODEL`), the validation fails. The CVM halts execution and triggers a **Lineage Violation (INT003)**.
