# CSEL-0005: Compiler Rejection Tests

## 1. Objective
To document test cases designed to verify that the CSEL compiler correctly detects, blocks, and rejects invalid cognitive constructs, type leaps, and invariant violations.

---

## 2. Epistemic Type Violations

### TEST-REJ-001: Direct Signal to Decision Leap
* **Description**: Verifies that the compiler blocks transitions that bypass intermediate context structuring, belief formation, and evidence verification.
* **CSEL Source Code**:
  ```csel
  ENTITY DirectAction {
      TYPE:
          OperationalConcept
      IDENTITY:
          cse://concept/direct_action
      TRANSFORMATION:
          Signal => Decision
  }
  ```
* **Expected Outcome**: Compilation abort.
* **Expected Error**: `CSE-TYPE-001: Illegal epistemic transition. Decision requires validated Knowledge state.`

---

## 3. Invariant Constraints Violations

### TEST-REJ-002: Meaning Lacking Context
* **Description**: Verifies the compiler enforces LAW CSE-005 (Relational Meaning), preventing isolated meaning assertions.
* **CSEL Source Code**:
  ```csel
  ENTITY IsolatedMeaning {
      TYPE:
          Concept
      IDENTITY:
          cse://concept/isolated_meaning
      CONSTRAINTS:
          requires cse://concept/std.observer
      TRANSFORMATION:
          Signal => Meaning
  }
  ```
* **Expected Outcome**: Compilation abort.
* **Expected Error**: `CSE-TYPE-003: Observer Frame/Context missing. Meaning cannot exist in isolation.`

---

## 4. Lineage Violations

### TEST-REJ-003: Knowledge without Lineage (CSA Breach)
* **Description**: Verifies the compiler blocks knowledge assertions that fail to trace lineage back to observers or evidence (violating LAW CSE-003).
* **CSEL Source Code**:
  ```csel
  ENTITY UnfoundedKnowledge {
      TYPE:
          Concept
      IDENTITY:
          cse://concept/unfounded_knowledge
      TRANSFORMATION:
          Belief => Knowledge
      LINEAGE:
          none
  }
  ```
* **Expected Outcome**: Compilation abort.
* **Expected Error**: `CSE-CONSTRAINT-003: Lineage path missing. Every knowledge node requires CSA lineage verification.`
