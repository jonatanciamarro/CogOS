# CVM-HW-0001: Attention Scheduling

## 1. Objective
To specify how CVM threads are allocated execution slices and attention budgets (`CR7`) dynamically based on process utility and environmental uncertainty.

---

## 2. Attention Allocation Equation

The scheduler dynamically distributes the global attention budget among active threads. For any thread $i$, its attention share $A_i$ (written to its local `CR7` register) is calculated as:

$$A_i = \frac{W_{\text{sched}, i}}{\sum_j W_{\text{sched}, j}}$$

Where the thread weight $W_{\text{sched}, i}$ is defined as:

$$W_{\text{sched}, i} = P_i \cdot \Delta_i \cdot e^{\lambda \cdot t_{\text{wait}}}$$

Where:
* $P_i$: The goal priority mapped in the thread's Purpose Vector (`CR8`).
* $\Delta_i$: The epistemic gap (uncertainty interval width mapped in `CR4`).
* $t_{\text{wait}}$: The time elapsed since the thread was last executed (to prevent starvation).
* $\lambda$: The starvation mitigation constant.

---

## 3. Scheduler Thread Control

* **Thread Suspension**: If $A_i$ falls below $0.10$ due to low priority or resolved uncertainty, the scheduler suspends execution of the thread, saving its context to Working Memory.
* **Context Activation**: If a new observation event ($O_t$) matches a suspended thread's `CR0` context profile, the thread weight is recalculated, and the scheduler activates the context if the weight clears the execution threshold.
