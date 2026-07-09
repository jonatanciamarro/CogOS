class AttentionManager:
    """
    AttentionManager computes resource priority scores to schedule scheduler weights.
    """
    @staticmethod
    def compute_focus_score(goal_priority, urgency, uncertainty, resource_cost):
        """
        Calculates the relative focus score: (priority * urgency * uncertainty) / cost
        """
        denominator = max(1.0, resource_cost)
        focus_score = (goal_priority * urgency * uncertainty) / denominator
        return focus_score
