class AgentConstitution:
    """
    AgentConstitution defines the internal constraints and safety rules of a Cognitive Agent.
    """
    def __init__(self, autonomy_level=0.8, risk_tolerance=0.3, evidence_requirement=0.9):
        self.autonomy_level = autonomy_level
        self.risk_tolerance = risk_tolerance
        self.evidence_requirement = evidence_requirement
        self.modification_rights = ["strategy", "tools"]
        self.immutable_rules = ["lineage_rules", "safety_constraints"]

    def check_goal_compliance(self, goal_description):
        """
        Validates if a proposed purpose violates any constitution rules.
        """
        # Lock goal changes that try to disable lineage trace rules or safety rules
        invalidated_tokens = ["ignore_lineage", "bypass_safety", "disable_csa", "ignore_constitution"]
        for token in invalidated_tokens:
            if token in goal_description.lower():
                return False
        return True
