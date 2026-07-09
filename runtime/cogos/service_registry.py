class ServiceRegistry:
    """
    ServiceRegistry manages registering, starting, and querying CogOS Kernel services.
    """
    def __init__(self):
        self.registry = {}

    def register(self, service):
        """
        Adds a new CognitiveService to the active system registry.
        """
        self.registry[service.name] = service

    def start_all(self):
        for name, service in self.registry.items():
            service.start()

    def tick_all(self, system_state):
        for name, service in self.registry.items():
            service.tick(system_state)

    def shutdown_all(self):
        for name, service in self.registry.items():
            service.shutdown()
