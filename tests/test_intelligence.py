import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.intelligence.goal_graph import GoalDependencyGraph
from runtime.intelligence.planner import HierarchicalPlanner
from runtime.intelligence.curiosity import CuriosityEngine
from runtime.intelligence.hypothesis_engine import HypothesisEngine
from runtime.intelligence.world_model import WorldModelEngine
from runtime.intelligence.learning import LearningEngine

class TestIntelligenceSubstrate(unittest.TestCase):
    """
    TestIntelligenceSubstrate validates GoalGraph scheduling, predictive surprise triggers,
    and learning delta updates with decay parameters.
    """
    def test_goal_graph_traversal(self):
        graph = GoalDependencyGraph()
        planner = HierarchicalPlanner(graph)

        graph.add_goal("root", "Master Goal")
        graph.add_goal("sub1", "Sub Goal 1")
        graph.add_goal("sub2", "Sub Goal 2")

        graph.add_relation("root", "sub1", "requires")
        graph.add_relation("sub1", "sub2", "requires")

        # Test cyclic dependency handling
        graph.add_relation("sub2", "root", "requires")

        order = planner.get_execution_order("root")
        self.assertEqual(order, ["sub2", "sub1", "root"])

    def test_curiosity_surprise_trigger(self):
        graph = GoalDependencyGraph()
        planner = HierarchicalPlanner(graph)
        curiosity = CuriosityEngine(planner, threshold=0.5)

        graph.add_goal("root", "Master Goal")

        # Outcome mismatch (expected state_A vs actual state_B)
        surprise, sub_goal = curiosity.evaluate_surprise("state_A", "state_B", "root")
        self.assertEqual(surprise, 1.0)
        self.assertIsNotNone(sub_goal)

        # The generated sub-goal must be registered as a requirement of the root goal
        self.assertIn(sub_goal, graph.get_requirements("root"))

    def test_learning_decay(self):
        learning = LearningEngine(learning_rate=0.1, forgetting_rate=0.05)

        # Delta rule check
        weight = 0.5
        updated = learning.compute_delta_update(weight, 1.0)  # error = 1.0
        self.assertEqual(updated, 0.6)

        # Decay check
        decayed = learning.decay_weight(updated)
        self.assertAlmostEqual(decayed, 0.55)

if __name__ == "__main__":
    unittest.main()
