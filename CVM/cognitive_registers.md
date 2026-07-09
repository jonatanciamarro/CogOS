# CVM-0002: Cognitive Registers (CR0-CR8)

## 1. Objective
To specify the architecture, data structures, and operational boundaries of the Cognitive Virtual Machine (CVM) registers (`CR0` to `CR8`).

---

## 2. Register Architecture Table

| Register | Register Name | Structural Data Type | Operational Function / Scope |
| :--- | :--- | :--- | :--- |
| **CR0** | Context | Context | Stores environmental parameters, calibration scales, and active context limits. |
| **CR1** | Belief | Belief | Stores the candidate hypothesis or concept currently under evaluation. |
| **CR2** | Evidence | Evidence Buffer | Array of pointers to validated evidence nodes supporting `CR1`. |
| **CR3** | Decision Candidate | Decision | The candidate action gate configuration selected for execution. |
| **CR4** | Uncertainty | Epistemic Interval $[P_{\text{min}}, P_{\text{max}}]$ | Real-time tracker of the active thread's epistemic gap and ambiguity level. |
| **CR5** | Resource Budget | Numeric | The remaining token count, FLOPs, or computational allowance. |
| **CR6** | Lineage | Lineage Chain | Pointers to predecessor nodes and parent transformations (CSA enforcement). |
| **CR7** | Attention | Attention Vector ($0.00 - 1.00$) | The computational priority multiplier allocated to the active process. |
| **CR8** | Purpose Vector | Purpose | Mappings of Goal, Utility, Priority, and Constraints. |

---

## 3. CR8: Purpose Vector Specification

The Purpose Vector (`CR8`) governs the teleology of the execution context, defining *why* a process is running:

$$\text{CR8} = (G, U, P, \Gamma)$$

Where:
* **Goal ($G$)**: The target state representation (e.g., `minimize_semantic_drift`).
* **Utility ($U$)**: The valuation mapping equation used to arbitrate decisions (e.g., $U = \alpha \cdot \text{Accuracy} - \beta \cdot \text{Energy}$).
* **Priority ($P$)**: The relative system-wide importance of this process.
* **Constraints ($\Gamma$)**: Operational boundaries that the execution must satisfy (e.g. `uncertainty < 0.2`).

---

## 4. Register Invariants & Constraints

* **CR6 Lineage Compulsion**: Any instruction trying to write to `CR3` (Decision Candidate) must be preceded by a validator check verifying that `CR6` contains a traceable path back to verified observations or invariants (violating this triggers a Lineage Violation interrupt).
* **CR7 Attention Decay**: If `CR7` drops below $0.10$ due to lack of reinforcement or priority reassignment, execution of the thread is immediately suspended by the Scheduler.
