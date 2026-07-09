# CogOS Architecture Guide

This guide establishes the division of responsibilities and architectural boundaries within the CogOS Cognitive Ecosystem. Use this to avoid accidental complexity and design drift during expansion.

---

## 1. Responsibility Boundary Matrix

| Component / Layer | Primary Responsibility | Allowed Interactions | Strict Constraints (NEVER DO) |
| :--- | :--- | :--- | :--- |
| **Simulation** | Runs simulation tick loops, manages kernel state transitions (BOOT/RUNNING/etc.), parses config presets, schedules and executes tick pipelines. | Reads config, triggers pipelines, ticks simulation kernel. | **Never** embed domain logic (science, culture, economy, politics) directly inside the Simulation. |
| **World** | Represents the global physical/spatial container. Dispatches global environment ticks. | Manages global systems (Climate, Global Resource Flows). | **Never** queue tasks, manage agent cognition, or control execution state loops. |
| **Civilization** | Orchestrates settlements and propagates local epochs (`EPOCH_ADVANCED`). | Contains and ticks local Settlements. | **Never** manage agent cognition directly, or execute global resource flow algorithms. |
| **Settlement** | Local community grouping. Manages local population collections. Ticks agent cognitive loop phases safely. | Ticks local environment systems (ResourcePool, RandomEvents). | **Never** modify global systems (like Climate) directly. |
| **Agent** | Individual entity reasoning, planning, memory storage, budget consumption. | Updates private memory segments, consumes personal budgets. | **Never** query or modify scheduler priorities directly. |
| **PipelineStage** | Defines the atomic steps of a single simulation tick. Ordered sequentially (or via DAG). | Reads context parameters, mutates shared stage state, dispatches domain logic. | **Never** store persistent simulation state internally. Must be stateless. |
| **EnvironmentSystem** | Advances a single slice of physical/economic environmental state. | Mutates local or global resource parameters. | **Never** call executors, schedule tasks, or directly invoke agent cognitive loops. |

---

## 2. Dynamic Extensions: The Extension Types

To keep the codebase comprehensible, CogOS differentiates strictly between extension mechanisms:

```
┌────────────────────────────────────────────────────────┐
│                        Contracts                       │
│              (PEP 544 structural interfaces)            │
└───────────────────────────┬────────────────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         ▼                                     ▼
 ┌──────────────┐                       ┌──────────────┐
 │   Registry   │                       │   EventBus   │
 │   Services   │                       │    Events    │
 └──────┬───────┘                       └──────┬───────┘
        │                                      │
        ├─► PipelineStages (Execution flow)    ├─► Telemetry (Observer-only)
        ├─► Systems        (Environment flow)  └─► Culture/Reputation (Decoupled)
        └─► Policies       (Cognitive choices)
```

1. **Contracts (Protocols)**: structural Python `Protocols` defining subsystem interfaces. Located in `runtime/contracts/`.
2. **Registry Services**: Singleton engines implementing contracts (e.g. `GreedyPolicy`, `KnowledgeRepository`).
3. **PipelineStages**: Execution sequence steps (e.g. `ObserveStage`, `ScienceStage`). Resolvable from the registry.
4. **EnvironmentSystems**: Pluggable environment simulations (e.g. `ClimateSystem`).
5. **Policies**: Pluggable strategies injected into registry services (e.g., `ScientificPolicy` vs. `MarketPolicy`).

---

## 3. Communication Strategy: Decoupling Rules

1. **No Concrete Domain Imports**: A domain module (e.g., `economy`) must never import another domain module directly (e.g., `science`). All cross-domain interaction goes through a structural contract (`Protocol`), is requested via `ServiceRegistry`, or is broadcasted asynchronously/synchronously via the `EventBus`.
2. **Telemetry decodes events**: Do not write direct calls to telemetry inside domain logic. Instead, Telemetry acts as a pure observer subscribing to `EventBus` channels.
3. **Task ROI Sorting**: Every executed process runs as a task ordered by its estimated ROI (priority divided by cost estimate) to prevent execution monopolization.

---

## 4. Concurrency: Synchronous vs. Asynchronous Events

The `EventBus` supports three publication semantics:
- `publish()`: Default routing (currently sync).
- `publish_sync()`: Immediate inline dispatch. Best for actions that must modify state sequentially.
- `publish_async()`: Background thread-pool dispatch. Best for non-blocking notifications, persistence, and telemetry monitoring.
