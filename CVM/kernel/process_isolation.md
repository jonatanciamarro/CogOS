# CVM-KERN-0004: Process Isolation

## 1. Objective
To specify the mechanisms through which the CVM isolates the memory spaces and lineage scopes of cognitive processes, preventing cross-thread corruption and semantic contamination.

---

## 2. Epistemic Address Space (EAS)

Each cognitive process executes within an isolated memory segment called the **Epistemic Address Space (EAS)**:

```text
       ┌─────────────────────────────────────────┐
       │         Epistemic Address Space         │
       └─────────────────────────────────────────┘
            │                               │
            ▼                               ▼
       ┌────────────────────────┐      ┌────────────────────────┐
       │   Private Local Graph  │      │   Shared Global Graph  │
       │  (CR0-CR8, Workspace)  │      │  (Read-Only Semantics)  │
       └────────────────────────┘      └────────────────────────┘
```

* **Private Segment**: Contains the local register values (`CR0` to `CR8`) and temporary working belief nodes. The kernel blocks other processes from reading or writing within this segment.
* **Shared Segment**: Contains pointers to the global Semantic and Episodic Memory graph. Standard processes may read from this segment (`E-READ` permission) but cannot write directly to it.

---

## 3. Lineage & Speculation Isolation

To prevent unverified or hallucinated beliefs from leaking across threads, the kernel enforces two isolation constraints:

1. **Speculation Shield**: A process cannot read the active `CR1` (Belief) or `CR4` (Uncertainty) registers of another concurrent process. It may only read stabilized knowledge nodes committed to Semantic Memory.
2. **Lineage Path Verification**: When a process submits a decision candidate to the kernel, the resource validator checks the process's lineage registry (`CR6`). It confirms that all ancestor references are fully contained within the caller's EAS or verified global nodes. Any cross-thread reference to an unverified private belief triggers a Lineage Violation (INT003) and aborts the write.
