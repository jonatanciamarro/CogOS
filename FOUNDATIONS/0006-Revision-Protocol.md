# FOUNDATIONS-0006: Revision Protocol

## 1. Objective
To define the rules for modifying, deprecating, merging, or splitting Cognitive Primitives and Theories in response to new observations, simulations, and empirical evidence.

---

## 2. Triggers for Revision

An epistemic revision process is automatically triggered under the following conditions:

1. **Epistemic Decay**: The confidence score of an active primitive falls below $0.3$ due to test failures or refuting evidence.
2. **Epistemic Division (Ambiguity Overload)**: A primitive accumulates high evidence counts, but its belief interval remains highly ambiguous (e.g., $[0.45, 0.55]$). This indicates the primitive is trying to model two distinct, conflated phenomena.
3. **Upstream Invalidation**: A parent primitive upon which this primitive depends (`DEPENDS ON`) is modified, refuted, or downgraded.

---

## 3. Structural Operations on Primitives

Revisions must conform to one of four formal structural operations:

* **Evolution**: Incremental updates to properties or predictions, maintaining a linear lineage:
  $$\text{Primitive}_{v1} \xrightarrow{\text{Evolution}} \text{Primitive}_{v2}$$
* **Split**: Dividing a single, ambiguous primitive into two or more distinct child primitives with separate scopes:
  $$\text{Primitive}_A \xrightarrow{\text{Split}} \text{Primitive}_{A1} + \text{Primitive}_{A2}$$
* **Merge**: Combining two separate, redundant primitives into a single unified construct:
  $$\text{Primitive}_{B1} + \text{Primitive}_{B2} \xrightarrow{\text{Merge}} \text{Primitive}_{B3}$$
* **Deprecation**: Moving a refuted or obsolete primitive into the inactive/archived space:
  $$\text{Primitive}_C \xrightarrow{\text{Deprecation}} \text{Archive}$$

---

## 4. Lineage and Ancestry Logging

To preserve semantic history, every modified primitive must write its ancestry variables using the Cognitive Primitive DSL syntax:

* `derived_from`: The ID of the direct predecessor.
* `creates`: The ID(s) of any primitives spawned from this node.
* `invalidates`: The ID(s) of obsolete primitives replaced by this node.
