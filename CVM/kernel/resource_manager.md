# CVM-KERN-0003: Resource Manager

## 1. Objective
To specify how the Cognitive Kernel monitors, limits, and manages the allocation of computational resources, memory, and energy among active execution threads.

---

## 2. Quota Management

The Resource Manager enforces strict limits over the values tracked in each process's Resource Budget (`CR5`) register:

* **Compute Quota**: The maximum number of CVM clock cycles or inference tokens a thread may consume before yielding control back to the scheduler.
* **Memory Quota**: The maximum number of graph vertices and edges a thread may allocate within its active Working Memory block.
* **Energy Quota**: The maximum thermodynamic cost allocation for the process lifecycle.

---

## 3. Exhaustion & Allocation Arbitration

When a thread's local `CR5` budget is depleted ($E \le 0$), the Resource Manager executes the following resolution loop:

1. **Trigger INT002**: Halt the execution loop of the thread and transfer control to the Resource Handler.
2. **Evaluate Purpose**: The manager inspects the thread's Purpose Vector (`CR8`).
   * **High Priority / Critical Invariant Goal**: The manager performs an **Energy Transfer**, reclaiming unused resource quotas from low-priority, idle threads and allocating them to the critical thread.
   * **Low Priority Goal**: The manager denies allocation. The thread is transitioned to the `SUSPENDED` state, and its local memory allocations are swept by the Epistemic GC.
