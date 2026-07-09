# ONTOLOGY-0001: Namespaces & Identity Scheme

## 1. Objective
To define the permanent addressing scheme for all entities within the Cognitive Systems Engineering Reference Standard (CSERS), guaranteeing substrate-agnostic traceability.

---

## 2. Namespace Grammar

Every identifier within the ecosystem must resolve to the following uniform syntax:

```text
cse://[domain]/[name]
```

Where:
* **`cse://`**: The standard URI scheme prefix.
* **`[domain]`**: The organizational or epistemic boundary (e.g., `concept`, `law`, `invariant`, `theory`, `observer`, `experiment`, `actor`, `signal`).
* **`[name]`**: The semantic snake-case identifier of the entity.

---

## 3. Core Namespace Mapping

The primary domains of CSERS are resolved according to the following baseline mappings:

| Epistemic Domain | Target URI Example | Cognitive Type System (CTS) Type |
| :--- | :--- | :--- |
| **Concepts** | `cse://concept/meaning` | CTS: Concept |
| **Laws** | `cse://law/semantic_integrity` | CTS: Law |
| **Invariants** | `cse://invariant/traceability` | CTS: Invariant |
| **Theories** | `cse://theory/active_inference` | CTS: Theory |
| **Observers** | `cse://observer/human_evaluator` | CTS: Observer |
| **Experiments** | `cse://experiment/EXP-0042` | CTS: Experiment |
| **Actors** | `cse://actor/reference_cogos` | CTS: Runtime Entity |
| **Signals** | `cse://signal/SIG-9081` | CTS: Signal |
