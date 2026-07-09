class WorkingMemory:
    """
    WorkingMemory manages hot variables and real-time thread scratch spaces.
    """
    def __init__(self):
        self.nodes = {}

    def get(self, uri):
        return self.nodes.get(uri)

    def set(self, uri, properties):
        self.nodes[uri] = properties
