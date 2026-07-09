from runtime.core.cvm_state import CVMState

class MachineContext:
    """
    MachineContext acts as the central coordinator binding the CVMState with the LKB Memory subsystems.
    """
    def __init__(self):
        self.state = CVMState()
        
        # Instantiate memory partitions
        self.working_memory = {}
        self.semantic_memory = {}
        self.episodic_memory = {}
        self.genetic_memory = {}

    def get_node(self, uri):
        """
        Retrieves a node from graph memory based on its URI prefix.
        """
        if not uri:
            return None
            
        if uri.startswith("cse://working/"):
            return self.working_memory.get(uri)
        elif uri.startswith("cse://semantic/") or uri.startswith("cse://concept/"):
            return self.semantic_memory.get(uri)
        elif uri.startswith("cse://episodic/") or uri.startswith("cse://observation/"):
            return self.episodic_memory.get(uri)
        elif uri.startswith("cse://genetic/"):
            return self.genetic_memory.get(uri)
        else:
            # Check semantic memory as fallback for standard concepts
            return self.semantic_memory.get(uri)
            
    def store_node(self, partition, uri, properties):
        """
        Safely writes a node into the target memory partition.
        """
        properties["uri"] = uri
        if partition == "working":
            self.working_memory[uri] = properties
        elif partition == "semantic":
            self.semantic_memory[uri] = properties
            self.state.memory_metadata["node_count"] = len(self.semantic_memory)
        elif partition == "episodic":
            self.episodic_memory[uri] = properties
        elif partition == "genetic":
            self.genetic_memory[uri] = properties
        else:
            raise KeyError(f"Invalid memory partition: {partition}")
