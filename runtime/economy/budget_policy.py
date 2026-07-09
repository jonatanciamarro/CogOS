class BudgetPolicy:
    """
    Configurable initial resource budgets — no hardcoded values in agent logic.
    """
    FOUNDER = {
        "cpu": 5000, "memory": 2048, "attention": 100, "energy": 100
    }
    STANDARD = {
        "cpu": 1000, "memory": 512, "attention": 25, "energy": 25
    }
    SPECIALIST = {
        "cpu": 2000, "memory": 1024, "attention": 50, "energy": 50
    }

    @staticmethod
    def for_role(role: str) -> dict:
        mapping = {
            "founder":    BudgetPolicy.FOUNDER,
            "standard":   BudgetPolicy.STANDARD,
            "specialist":  BudgetPolicy.SPECIALIST,
        }
        return dict(mapping.get(role, BudgetPolicy.STANDARD))
