# canon - The Vocabulary & Grammar of CSE

This directory defines the syntax, algebra, and classification systems of Cognitive Systems Engineering (CSE). The files here serve as the linguistic and logical guidelines for any cognitive node added to CogOS.

---

## Contents

* **[canon/README.md](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/canon/README.md)**: Specification of the Cognitive Primitive DSL.
* **[canon/algebra.md](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/canon/algebra.md)**: The rules of cognitive transformation algebra.
* **[canon/negative_space.md](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/canon/negative_space.md)**: The classification of unknown, unobserved, and impossible structures.

---

## Cognitive Primitive DSL Specification

Any active node of knowledge, law, invariant, or hypothesis within the repository must be written using the following domain-specific grammar to allow machine parsing, validation, and lineage checking:

```text
PRIMITIVE [Unique-ID]
TYPE: Concept | Invariant | Law | Transformation | Hypothesis
TITLE: "[Human Readable Name of the Primitive]"
PURPOSE: "[Teleological declaration: why this concept exists and its evolutionary necessity]"
OBSERVER: [Observing node or frame reference]
CONFIDENCE: [Rational value between 0.00 and 1.00]

ASSUMES:
  - "[Epistemic assumption or postulate 1]"
  - "[Epistemic assumption or postulate 2]"

DEPENDS ON:
  - [Predecessor Primitive ID A]
  - [Predecessor Primitive ID B]

GENERATES:
  - [Derived Primitive ID C]

INVALIDATES:
  - [Refuted Primitive ID D]

PREDICTS:
  - "[Specific, falsifiable prediction of what will happen under condition X]"

TESTABLE_BY:
  - "[Reference to experiment protocol or test framework]"

EVIDENCE:
  - "[Documented observation or result verifying the prediction]"

COUNTEREXAMPLES:
  - "[Documented observations where the prediction failed]"

FAILURE_MODES:
  - "[Boundary conditions where this concept collapses or ceases to apply]"
```
