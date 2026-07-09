class EpisodicMemory:
    """
    EpisodicMemory stores transient signals, observations, and experiment records.
    """
    def __init__(self):
        self.nodes = {}

    def get(self, uri):
        return self.nodes.get(uri)

    def set(self, uri, properties):
        self.nodes[uri] = properties
