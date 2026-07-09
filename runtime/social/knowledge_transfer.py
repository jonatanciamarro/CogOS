from runtime.intelligence.state_model import InternalBelief

class KnowledgeTransfer:
    """
    KnowledgeTransfer validates incoming messages, scaling claim confidence based on sender trust.
    """
    @staticmethod
    def ingest_claim(sender_id, message, trust_network):
        """
        Receives a claim and scales its confidence based on sender trust rating and lineage footprint.
        """
        trust = trust_network.get_trust_rating(sender_id)

        # Lineage scaling penalty: halved if lineage traces are empty
        lineage_multiplier = 1.00 if len(message.lineage) > 0 else 0.50

        scaled_confidence = message.confidence * trust * lineage_multiplier

        # Generate internal belief concept node
        belief = InternalBelief(message.claim, confidence=scaled_confidence)
        belief.evidence = list(message.lineage)
        return belief
