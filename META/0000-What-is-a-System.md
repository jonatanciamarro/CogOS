# META-0000: What is a System?

## 1. The Question
How do we define the boundaries, components, and interactions of a coherent structure (a "system") in Cognitive Systems Engineering (CSE), particularly when dealing with distributed, artificial cognitive ecosystems?

---

## 2. Competing Theories

### Theory A: Closed Cybernetic System (Structuralist)
* **Definition**: A system is a collection of discrete components with fixed inputs, outputs, and feedback loops operating within a predefined, static boundary.
* **Assumes**: Boundaries are physical or digital and defined externally by the architect. Component states are fully addressable and static.
* **Predicts**: Failures are localized to specific component states. The system cannot maintain structural integrity if component mappings are altered.
* **Testable By**: API fault-injection experiments measuring throughput degradation.

### Theory B: Autopoietic Cognitive Ecosystem (Emergentist)
* **Definition**: A system is a self-maintaining (autopoietic), self-bounding network of transformations whose boundaries are dynamically established by the interactions of its internal processes and observers.
* **Assumes**: Boundaries are fluid, defined by information density. Components are transient patterns of cognitive activity rather than fixed code blocks.
* **Predicts**: The system will dynamically re-route processes and construct new structural pathways to maintain homeostasis when node-paths are constrained.
* **Testable By**: Restricting traditional node communication in a simulated model network and observing emergent self-routing behaviors.

---

## 3. Evidence Matrix

| Phenomenon / Anomaly | Theory A (Cybernetic) | Theory B (Autopoietic) |
| :--- | :--- | :--- |
| **Explains self-healing routing** | Poor (requires manual failover paths) | Strong (predicted by self-bounding homeostatic rules) |
| **Integrates heterogeneous nodes** | Moderate (requires rigid translation wrappers) | Strong (nodes adapt dynamically via semantic gravity) |
| **Mathematical verification** | High (finite-state machine bounds) | Moderate (non-linear dynamical system equations) |

---

## 4. Current Best Theory
**Theory B (Autopoietic Cognitive Ecosystem)** is selected as the current best theory.

* **Justification**: Organizational intelligence does not reside in single databases or APIs; it is distributed, shifting, and ephemeral. A rigid, closed cybernetic model fails to explain how organizational meaning persists across infrastructure changes. Autopoietic boundaries permit the ecosystem to adapt to model degradation and context drift without complete structural failure.
