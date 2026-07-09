class CuriosityEngine:
    """
    CuriosityEngine computes prediction errors to calculate Surprise Scores and injects exploration sub-goals.
    """
    def __init__(self, planner, threshold=0.5):
        self.planner = planner
        self.threshold = threshold

    def evaluate_surprise(self, predicted_state, actual_state, current_goal_id=None):
        """
        Calculates surprise delta. Spawns investigation sub-goals when threshold is exceeded.
        """
        # If predicted state does not match actual state, surprise is maximum (1.0)
        surprise_score = 0.0 if predicted_state == actual_state else 1.0

        sub_goal_id = None
        if surprise_score >= self.threshold and current_goal_id:
            # Dynamic sub-goal injection into Goal Graph
            sub_goal_id = f"resolve_surprise_{predicted_state}_vs_{actual_state}"
            self.planner.goal_graph.add_goal(
                sub_goal_id, 
                f"Investigate surprise: expected {predicted_state}, observed {actual_state}"
            )
            self.planner.goal_graph.add_relation(current_goal_id, sub_goal_id, "requires")

        return surprise_score, sub_goal_id
