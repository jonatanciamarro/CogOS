from runtime.intelligence.state_model import InternalBelief

class MetaCognitionEngine:
    """
    MetaCognitionEngine audits local beliefs, penalizing high confidence supported by low evidence counts.
    """
    @staticmethod
    def audit_belief(belief):
        """
        Adjusts belief confidence downwards if evidence support is insufficient.
        """
        evidence_count = len(belief.evidence)
        
        # Bias constraint: high confidence (>0.7) with insufficient evidence (<2)
        if belief.confidence > 0.7 and evidence_count < 2:
            belief.update_confidence(0.4)
            return True  # Audited and corrected
            
        return False
