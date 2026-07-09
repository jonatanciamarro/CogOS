# experiments - Empirical Testing Protocols

This directory maps out the active experiment logs, protocol templates, and empirical evidence runs. Every prediction made by our cognitive primitives must be tested against these protocols to establish validity and update confidence scores.

---

## Contents

* **[experiments/README.md](file:///c:/Users/WDAGUtilityAccount/Downloads/projeto/experiments/README.md)**: Specifications for testing hypotheses and logging results.

---

## Experiment Logging Schema

Every empirical test run within the ecosystem must be documented in a separate file (e.g., `EXP-XXXX.md`) using the following structured grammar to enable automated confidence score updates:

```text
EXPERIMENT [EXP-Unique-ID]
HYPOTHESIS: [ID of the Hypothesis or Primitive under test]
DATE: [Execution Timestamp]
OBSERVER: [Observing node or logger ID]

PROTOCOL:
  1. "[Step-by-step experimental setup and environment variables]"
  2. "[Sensing controls and isolation parameters]"
  3. "[Measurement prompts, instrumentation, or scripts used]"

EXPECTED_OUTCOME:
  - "[Precise prediction matching the hypothesis' PREDICTS block]"

OBSERVED_OUTCOME:
  - "[Raw result logs, performance graphs, or output vectors]"

EVIDENCE_RATING:
  - LEVEL: [E-1 (Simulated) | E-2 (Controlled) | E-3 (Longitudinal)]
  - WEIGHT: [0.25 | 0.50 | 0.75]
  - SUPPORT (Se): [Support rating from -1.0 (refuted) to +1.0 (validated)]

CONFIDENCE_UPDATE:
  - PRIOR: [Confidence score before test execution]
  - POSTERIOR: [Updated confidence score calculated via the Evidence System formula]

AFFECTED_PRIMITIVES:
  - [IDs of Primitives validated, downgraded, or invalidated by this experiment]
```
