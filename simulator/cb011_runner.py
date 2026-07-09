import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.economy.budget_policy import BudgetPolicy
from runtime.economy.resource_budget import ResourceBudget
from runtime.economy.credit_economy import CreditLedger
from runtime.economy.market import IdeaMarket
from runtime.economy.resource_scheduler import ResourceScheduler
from runtime.economy.scheduling_policy import ScientificPolicy
from runtime.execution.task_queue import Task, TaskQueue
from runtime.execution.executor import Executor
from runtime.execution.rollback import RollbackManager
from runtime.cogos.resource_daemon import ResourceDaemon
from runtime.bus.event_bus import EventBus, CogOSEvents, EventPriority
from runtime.agents.agent import CognitiveAgent

class CB011Runner:
    """
    CB-011: Scientific Scarcity Benchmark.
    3 agents with STANDARD budgets must choose between exploring new hypotheses
    (high cost) vs. replicating known ones (low cost). Measures SE, BU, DUS.
    """
    @staticmethod
    def run_benchmark():
        print("=== Initializing CogOS Resource Economy Simulator: CB-011 ===")

        # Infrastructure
        bus = EventBus()
        market = IdeaMarket(idle_sweep_threshold=3)
        rollback = RollbackManager()

        # Event counters
        budget_exhaustions = [0]
        tasks_completed    = [0]

        bus.subscribe(CogOSEvents.BUDGET_EXHAUSTED,
                      lambda e, p: budget_exhaustions.__setitem__(0, budget_exhaustions[0]+1),
                      EventPriority.CRITICAL)

        # Spawn 3 agents with STANDARD budgets
        agents = []
        for name in ["Researcher", "Replicator", "Explorer"]:
            a = CognitiveAgent(name)
            a.resource_budget = ResourceBudget(BudgetPolicy.for_role("standard"))
            a.trust_score = 0.6
            a.historical_efficiency = 0.8
            agents.append(a)

        agents_by_id = {a.identity.agent_id: a for a in agents}

        # TaskQueue + Executor
        queue = TaskQueue()
        executor = Executor(queue, agents_by_id, event_bus=bus)

        # Register hypotheses in IdeaMarket
        market.register_hypothesis("cse://hyp/gravity_constant")
        market.register_hypothesis("cse://hyp/dark_energy_model")
        h1 = market.ideas["cse://hyp/gravity_constant"]
        h1.eig = 0.9; h1.impact_expected = 0.8; h1.risk = 0.2

        h2 = market.ideas["cse://hyp/dark_energy_model"]
        h2.eig = 0.5; h2.impact_expected = 0.6; h2.risk = 0.5

        ranked = market.rank_by_evi()

        # Submit tasks: explore top hypothesis (high cost) + replicate known (low cost)
        researcher = agents[0]
        replicator = agents[1]
        explorer   = agents[2]

        def record_done(): tasks_completed.__setitem__(0, tasks_completed[0]+1)

        queue.enqueue(Task("explore_top", researcher.identity.agent_id,
                           record_done, priority=2.0, cost_estimate=400,
                           urgency=0.9, expected_information_gain=0.9))

        queue.enqueue(Task("replicate_known", replicator.identity.agent_id,
                           record_done, priority=1.0, cost_estimate=80,
                           urgency=0.5, expected_information_gain=0.5))

        queue.enqueue(Task("explore_secondary", explorer.identity.agent_id,
                           record_done, priority=1.5, cost_estimate=1200,  # exceeds STANDARD budget
                           urgency=0.7, expected_information_gain=0.7))

        # Execute all tasks
        while len(queue) > 0 or True:
            executed = executor.run_next()
            if not executed:
                break

        # ResourceDaemon tick
        daemon = ResourceDaemon(event_bus=bus)
        daemon.tick(agents_by_id, idea_market=market)

        # Credit economy: researcher published, gets credits
        ledger = CreditLedger()
        ledger.award(CogOSEvents.PUBLICATION_ACCEPTED)
        ledger.convert_to_resources(researcher.resource_budget)

        # Compute metrics
        total_tasks    = 3
        completed      = tasks_completed[0]
        se  = completed / total_tasks                          # Scientific Efficiency
        bu  = 1.0 - (budget_exhaustions[0] / total_tasks)     # Budget Utilization (inverse failure rate)
        dus = completed / total_tasks                          # Discovery Under Scarcity

        top_hyp_id, top_evi = ranked[0]

        print("\n=============================================")
        print("         CB-011 BENCHMARK REPORT             ")
        print("=============================================")
        print(f" Scientific Efficiency (SE):   {se:.2f}   (not 1.00 by design)")
        print(f" Budget Utilization (BU):      {bu:.2f}")
        print(f" Discovery Under Scarcity (DUS): {dus:.2f}")
        print(f" Budget Exhaustions:           {budget_exhaustions[0]}")
        print(f" Top Hypothesis by EVI:        {top_hyp_id}")
        print(f" Top EVI Score:                {top_evi:.4f}")
        print(f" IdeaMarket ranking working:   {len(ranked) == 2}")
        print("=============================================\n")

        return se, bu, dus


if __name__ == "__main__":
    CB011Runner.run_benchmark()
