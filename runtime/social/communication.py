class CognitiveMessage:
    """
    CognitiveMessage defines the formatted claims, confidence values, and lineage records.
    """
    def __init__(self, sender_id, receiver_id, claim_concept, confidence=1.0, lineage=None):
        self.sender = sender_id
        self.receiver = receiver_id
        self.claim = claim_concept
        self.confidence = confidence
        self.lineage = lineage if lineage else []


class SocialCommunicationBus:
    """
    SocialCommunicationBus manages in-memory message routing between active agents.
    """
    def __init__(self):
        self.inboxes = {}  # receiver_id -> list of CognitiveMessage

    def transmit(self, message):
        """
        Delivers a CognitiveMessage to the recipient's inbox.
        """
        rec = message.receiver
        if rec not in self.inboxes:
            self.inboxes[rec] = []
        self.inboxes[rec].append(message)

    def fetch_messages(self, receiver_id):
        """
        Retrieves and clears all pending messages for the target recipient.
        """
        messages = self.inboxes.get(receiver_id, [])
        self.inboxes[receiver_id] = []
        return messages
