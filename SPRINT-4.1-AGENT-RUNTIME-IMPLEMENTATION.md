# CSERS SPRINT-4.1: Cognitive Agent Runtime Prototype (CARP) Implementation Plan

## 1. Abstract
This document outlines the detailed file structure, variables, classes, and verification routes for Sprint 4.1. We build the first autonomous cognitive agent running on the CVM.

---

## 2. Directory Layout & Proposed Changes

The prototype modules will be created under the workspace:

### Agent Model & Lifecycle (`runtime/agents/`)
* **[identity.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/identity.py)**: The `AgentIdentity` class containing UUID, lineage references, creation timestamps, and parent agent indicators. Immutability rules enforced.
* **[events.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/events.py)**: The central `AgentEventLog` auditing creation, suspension, and updates.
* **[agent.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/agent.py)**: The `CognitiveAgent` class coordinating identity, purpose_vector, process PIDs, and capabilities.
* **[agent_state.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/agent_state.py)**: Life states (CREATED, BOOTING, ACTIVE, REFLECTING, SUSPENDED, ARCHIVED) and `CognitivePhase` Enum.
* **[constitution.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/constitution.py)**: Decision-making weights and constraints.
* **[lifecycle.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/lifecycle.py)**: Spawn, suspend, resume, and archive operations.
* **[purpose_engine.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/purpose_engine.py)**: Validates CR8 Purpose updates via syscalls.
* **[purpose_history.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/purpose_history.py)**: Monotonic logs of goals mutations and Omega cost.
* **[capability.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/capability.py)**: Tool request wrappers.
* **[cognitive_loop.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/agents/cognitive_loop.py)**: Dynamic execution step (Observe $\to$ Interpret $\to$ Hypothesize $\to$ Action $\to$ Result $\to$ Reflect $\to$ Consolidate).

### Agent Private Memory Partitions (`runtime/memory/agent/`)
* **[strategy.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/memory/agent/strategy.py)**: Isolated strategy and planning logs.
* **[experience.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/memory/agent/experience.py)**: Local sensory learning logs.
* **[failures.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/memory/agent/failures.py)**: Refuted hypotheses.
* **[reflection.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/runtime/memory/agent/reflection.py)**: Insights and bias corrections.

### Simulator & Verification (`simulator/` & `tests/`)
* **[cb003_runner.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/simulator/cb003_runner.py)**: Benchmark runner calculating GCR, LE, SI, SRC, and Cognitive Continuity Score (CCS).
* **[test_agent_runtime.py](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/tests/test_agent_runtime.py)**: Unit tests for state persistency, child inheritance, process death survival, identity integrity, reflection propagation, and purpose mutation audits.
