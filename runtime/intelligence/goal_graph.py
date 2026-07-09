class GoalNode:
    """
    GoalNode represents a specific target milestone inside the GoalGraph.
    """
    def __init__(self, goal_id, description, status="PENDING"):
        self.id = goal_id
        self.description = description
        self.status = status  # PENDING, IN_PROGRESS, COMPLETED, FAILED


class GoalDependencyGraph:
    """
    GoalDependencyGraph manages dependent goals and constraints, supporting cyclic references.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []  # List of tuples: (source_id, target_id, relation_type)

    def add_goal(self, goal_id, description):
        node = GoalNode(goal_id, description)
        self.nodes[goal_id] = node
        return node

    def add_relation(self, source_id, target_id, relation_type="requires"):
        """
        Adds links like: Goal A 'requires' Goal B, or Goal A 'conflicts' Goal C.
        """
        self.edges.append((source_id, target_id, relation_type))

    def get_requirements(self, goal_id):
        """
        Retrieves all immediate prerequisites for a given goal node.
        """
        return [target for source, target, rel in self.edges if source == goal_id and rel == "requires"]
