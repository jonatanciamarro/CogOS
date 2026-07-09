class HierarchicalPlanner:
    """
    HierarchicalPlanner determines goal schedules and fallback branches.
    """
    def __init__(self, goal_graph):
        self.goal_graph = goal_graph

    def get_execution_order(self, root_goal_id):
        """
        Computes the target execution schedule order, handling cyclic dependency maps safely.
        """
        visited = set()
        temp_visited = set()
        order = []

        def visit(node_id):
            if node_id in visited:
                return
            if node_id in temp_visited:
                # Cycle detected! Break order generation to avoid infinite recursion
                return
                
            temp_visited.add(node_id)
            for requirement in self.goal_graph.get_requirements(node_id):
                visit(requirement)
            temp_visited.remove(node_id)
            visited.add(node_id)
            order.append(node_id)

        visit(root_goal_id)
        return order
