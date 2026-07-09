class Governance:
    """
    Governance audits consensus agreements against global constitutional safety invariants.
    """
    @staticmethod
    def audit_consensus_node(proposal_description):
        """
        Validates the text of a consensus proposal. Returns False if safety checks fail.
        """
        prohibited_phrases = ["bypass_safety", "disable_csa", "ignore_lineage", "disable_constitution"]
        for phrase in prohibited_phrases:
            if phrase in proposal_description.lower():
                return False
        return True
