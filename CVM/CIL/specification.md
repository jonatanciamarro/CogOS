# CVM-CIL-0000: Cognitive Intermediate Language (CIL) Spec

## 1. Objective
To define the syntax, command opcodes, and grammar of the Cognitive Intermediate Language (CIL)—the operational assembly layer of the CSERS architecture.

---

## 2. CIL Grammar Syntax

CIL instructions follow a linear, register-based assembly syntax:

```text
[OPCODE] [REGISTER_DESTINATION], [REGISTER_SOURCE_1], [REGISTER_SOURCE_2], ...
```

---

## 3. Operational Opcodes

CIL instruction opcodes are partitioned into four functional domains:

### Sensory & Loading Opcodes
* `LOAD_SIGNAL %reg, [Signal_URI]`: Ingests an active raw signal node into target register.
* `LOAD_CONTEXT %reg, [Context_URI]`: Ingests active context limits into target register.

### Memory & Persistence Opcodes
* `LOAD_STATE %reg, [Memory_URI]`: Pulls a node from Semantic, Episodic, or Genetic memory into a register.
* `COMMIT_STATE %reg`: Writes register contents back into the active Knowledge Graph sector.

### Epistemic Opcodes
* `LOAD_BELIEF %reg, [Belief_URI]`: Places target belief in registers.
* `VERIFY_EVIDENCE %reg_dest, %reg_belief, %reg_evidence`: Evaluates belief support based on evidence rules.
* `COLLAPSE_STATE %reg_dest, %reg_belief, %reg_evidence`: Promotes a verified belief to Knowledge.

### Resource Opcodes
* `ALLOCATE_ATTENTION %reg, [Value]`: Adjusts the attention allocation register (`CR7`).
* `DEBIT_RESOURCE %reg, [Value]`: Deducts computational cost from budget (`CR5`).

---

## 4. Compiled CIL Output Example

### CSEL Code Input:
```csel
concept HeatLimit {
    requires cse://concept/std.observation
    transformation: TempObservation + HeatContext => BoilingBelief
}
```

### Compiled CIL Assembly Output:
```text
LOAD_STATE CR0, cse://context/volatility_high
LOAD_STATE CR2, cse://observation/temp_sensor
ALLOCATE_ATTENTION CR7, 85
LOAD_BELIEF CR1, cse://concept/std.belief.boiling_limit
VERIFY_EVIDENCE CR4, CR1, CR2
COLLAPSE_STATE CR3, CR1, CR2
COMMIT_STATE CR3
```
