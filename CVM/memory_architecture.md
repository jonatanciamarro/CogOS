# CVM-0005: Memory Architecture & Epistemic GC

## 1. Objective
To specify the organization of the CVM Graph Memory and detail the rules of the Epistemic Garbage Collector (GC).

---

## 2. Memory Partitions

CVM memory is segmented into four distinct conceptual stores to isolate active reasoning from historical and structural records:

```text
       ┌─────────────────────────────────────────┐
       │             Cognitive Memory            │
       └─────────────────────────────────────────┘
            │          │           │          │
            ▼          ▼           ▼          ▼
       ┌─────────┐┌──────────┐┌─────────┐┌─────────┐
       │ Working ││ Semantic ││Episodic ││ Genetic │
       └─────────┘└──────────┘└─────────┘└─────────┘
```

### 1. Working Memory
* **Scope**: Stores active registers (`CR0` to `CR8`), hot context variables, and active belief nodes currently evaluated by execution threads.
* **Constraints**: Subject to real-time attention budgets (`CR7`). If attention decays, nodes are flushed.

### 2. Semantic Memory
* **Scope**: Houses stabilized ontologies, conceptual definitions, invariants, schemas, and laws of the LKB.
* **Constraints**: Read-only during standard execution. Modifications require explicit `Evolution` instructions.

### 3. Episodic Memory
* **Scope**: Stores observation history, raw signal logs, and execution trace logs.
* **Constraints**: Retains raw data inputs that generated belief updates.

### 4. Genetic Memory
* **Scope**: Stores the lineage history and ancestry genealogy of all primitives (`EvolvedFrom`, `Supersedes`).
* **Constraints**: Read-only segment. Preserves historical audits.

---

## 3. Class Transition Rules

To prevent cognitive inflation and false stabilization (generalizing from a single observation), no data may change class without a formal CSEL command. Specifically, transitioning from Episodic Memory (raw experience) to Semantic Memory (universal law) requires executing a `GENERALIZE` instruction, satisfying:

1. **Evidence Volume**: Minimum of $N$ distinct observations.
2. **Predictive Verification**: Complete verification of associated predictions.
3. **Trust Rating**: Trust rating of observing nodes above threshold.

---

## 4. Epistemic Garbage Collector (GC)

The Epistemic GC prevents context explosion by running four sequential passes:

* **MARK**: Scans the LKB graph starting from invariants (`CONSTITUTION`) and current purpose registers (`CR8`). Marks active dependencies.
* **SWEEP**: Locates unmarked nodes that have no active attention weight. Sweeps them to cold storage (Dormant level).
* **COMPRESS**: Evaluates clusters of low-level, redundant observations. Fuses them into higher abstractions (Semantic Compression).
* **ARCHIVE**: Flags refuted nodes and obsoleted models, moving them to Genetic Memory for provenance tracking and replacing active pointers.
