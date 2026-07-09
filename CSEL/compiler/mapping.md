# CSEL-0004: CSEL to KIR Compiler Mapping

## 1. Objective
To define the formal translation rules mapping CSEL source declarations and transformation equations into AST structures and optimized KIR nodes.

---

## 2. AST Representation and Node Creation

The compiler maps CSEL block headers to AST Node properties:

1. **Entity Declarations**:
   ```csel
   ENTITY Observation { TYPE: AbstractConcept }
   ```
   maps to a typed node definition in the semantic graph:
   ```text
   Node(id=cse://concept/std.observation, type=AbstractConcept)
   ```

2. **Metadata Binding**:
   Properties like `CONFIDENCE` and `LINEAGE` are bound directly to the target node's metadata attributes.

---

## 3. Transformation Compilation (CSA Generation)

The compiler compiles relational CSEL equations into unique CSA-assigned instruction nodes in KIR:

```csel
TRANSFORMATION:
    Signal + Context + Observer => Observation
```

Is mapped to a compiler instruction template:

```text
%obs_id = cse://concept/std.observation [confidence]
    = OBSERVE %sig_id, %obs_id, %ctx_id
    {
        lineage: %sig_id
    }
```

---

## 4. Constraint Enforcement Mapping

CSEL invariants are translated into compiler-enforced assertions:

```csel
INVARIANT:
    ObservationWithoutObserver = INVALID
```

Generates a validation pass rule:

```text
VALIDATE:
    IF NOT EXISTS (cse://concept/std.observer IN dependencies(%obs_id)):
        COMPILE_ERROR "CSE-CONSTRAINT-002: Invariant violated. Observation requires Observer."
```
