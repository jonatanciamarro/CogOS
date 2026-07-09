# CVM-HW-0000: Interrupt Vector Table

## 1. Objective
To specify the Interrupt Vector Table (IVT) of the CVM, defining the handling routes and priorities for core system events and cognitive faults.

---

## 2. Interrupt Vector Table

The CVM implements five standard interrupt channels to capture operational anomalies:

| Vector Code | Interrupt Name | Trigger Event | Priority | Default Handler Action |
| :--- | :--- | :--- | :--- | :--- |
| **INT001** | Contradiction Found | Competing active nodes detected. | 2 (High) | Pause execution thread. Set target node states to `Under Review`. Trigger Epistemic Arbitration. |
| **INT002** | Resource Depleted | `CR5` (Resource Budget) drops below threshold. | 3 (Medium) | Suspend process context. Trigger scheduler queue rebalancing. Trigger Epistemic GC. |
| **INT003** | Lineage Violation | Attempt to write to decision registers without a valid CSA trace. | 1 (Critical) | Abort active thread. Flag transaction as invalid in the log. |
| **INT004** | Uncertainty Explosion | Epistemic Gap width $\Delta$ exceeds constraint limit. | 4 (Low) | Suspend decision gate. Request active evidence search. |
| **INT005** | Memory Corruption | Graph consistency check failure. | 1 (Critical) | Halt the CVM. Trigger rollback to the last verified snapshot. |

---

## 3. Interrupt Handling Semantics

When an interrupt is triggered, the execution unit processes it using three sequential steps:

1. **Context Save**: The current values of registers `CR0` to `CR8` and the Instruction Pointer (`CIP`) are pushed onto the Working Memory thread stack.
2. **Vector Dispatch**: Execution is routed to the handler function registered in the IVT.
3. **Resume or Abort**: If the handler resolves the anomaly (e.g., arbitration completes or resources are allocated), the context is popped and execution resumes; if critical (INT003 or INT005), the thread is aborted to prevent epistemic corruption.
