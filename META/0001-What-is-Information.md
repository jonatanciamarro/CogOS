# META-0001: What is Information?

## 1. The Question
What is the fundamental nature of information in Cognitive Systems Engineering? Is it purely probabilistic state reduction, or is it bound to semantic distinction?

---

## 2. Competing Theories

### Theory A: Shannon-Wiener Information (Syntactic/Statistical)
* **Definition**: Information is the mathematical reduction of statistical uncertainty, measured in bits of entropy, independent of the meaning or truth of the content.
* **Assumes**: Information is purely syntactic. The cognitive value of a message is equivalent to its probability of occurrence.
* **Predicts**: System bandwidth and cognitive capacity are optimized solely by reducing syntactic transmission redundancy.
* **Testable By**: Measuring compression ratios and bit-error rates over simulated communication lines.

### Theory B: Bateson-Floridi Information (Semantic/Difference)
* **Definition**: Information is "a difference which makes a difference" (Bateson)—data that is well-formed, semantically grounded, and relevant to the observer's world model.
* **Assumes**: Information is relational and requires semantic structure. Untruthful or irrelevant signals do not constitute cognitive information.
* **Predicts**: Transmitting high-entropy random signals will fail to alter the recipient's belief states, whereas a low-entropy structured signal will trigger major cognitive state changes.
* **Testable By**: Injecting equal-bit streams of coherent vs. chaotic text into a decision-making loop and measuring the delta in the belief interval.

---

## 3. Evidence Matrix

| Phenomenon / Anomaly | Theory A (Shannon) | Theory B (Bateson-Floridi) |
| :--- | :--- | :--- |
| **Explains network capacity** | Strong (provides absolute channel capacity limits) | Poor (cannot quantify physical channel bounds) |
| **Explains relevance filtering** | Poor (treats high-noise spam and high-value signals equally if entropy matches) | Strong (defines information relative to observer relevance) |
| **Explains semantic drift** | Poor (bit distributions can remain identical while meanings shift) | Strong (models drift as changes in semantic relationships) |

---

## 4. Current Best Theory
**Theory B (Bateson-Floridi Information)** is selected as the current best theory for cognitive operations, using **Theory A** as a subordinate physical constraints model.

* **Justification**: In CSE, our core concern is how ecosystems evaluate and act on data. Shannon information is indispensable for managing data packets, but it is blind to meaning. If a system receives a verified fact or a hallucination, Shannon entropy treats them identically. CSE requires a definition of information that is grounded in meaning and relational difference.
