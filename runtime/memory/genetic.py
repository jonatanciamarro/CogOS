class GeneticMemory:
    """
    GeneticMemory preserves immutable version lineages of deprecated/evolved nodes.
    """
    def __init__(self):
        self.nodes = {}

    def get(self, uri):
        return self.nodes.get(uri)

    def set(self, uri, properties):
        self.nodes[uri] = properties
