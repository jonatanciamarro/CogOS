# temporal - The Physics of Cognitive Time

## 1. Objective
To define the temporal dynamics of the cognitive ecosystem, treating time as a constraint that causes decay, context shift, and evolution of knowledge.

---

## 2. Temporal Decay of Evidence

Evidence is not static. Its weight and relevance to active beliefs decays over time as the environment evolves:

$$W_e(t) = W_e(0) \cdot e^{-\lambda \cdot t}$$

Where:
* $W_e(0)$ is the initial weight of the evidence (defined in the Evidence Scale).
* $\lambda$ is the decay constant of the specific domain (highly volatile environments have a larger $\lambda$).
* $t$ is the elapsed time since the observation was recorded.

When the decaying weight $W_e(t)$ drops below $0.10$, the associated primitive triggers a re-validation event to check if the underlying assumptions still match current signals.

---

## 3. Epistemic Expiration

We define three classes of temporal lifespans for knowledge in the system:

1. **Volatile Contexts**: Expiry scale is measured in seconds/minutes (e.g., operational metrics, database states).
2. **Structural Beliefs**: Expiry scale is measured in days/weeks (e.g., heuristics, market patterns, system configurations).
3. **Core Axioms & Invariants**: Expiry scale is infinite (stable principles that govern the physics of the system).

Upon expiration, a primitive is downgraded from `Knowledge` back to the `UNOBSERVED` negative space.

---

## 4. Observer History Drift

An observer frame of reference shifts as it records data and learns. Consequently, a measurement made at time $t_0$ may not yield the same semantic result at time $t_1$, even under identical signal inputs. 

To resolve this, every recorded signal, belief, and transformation must log a dual stamp:
* The **System Time** ($t$).
* The **Observer Version** ($V_{obs}$), representing the state of the observer's ontology when the distinction was made.
