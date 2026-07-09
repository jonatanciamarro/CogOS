from typing import Type, TypeVar

T = TypeVar("T")


class ServiceRegistry:
    """
    ServiceRegistry resolves subsystem implementations by Protocol type.
    Hot-swappable: Sprint 5.1 registers MarketProtocol without touching RuntimeContext.

    Usage:
        registry.register(SchedulerProtocol, GreedyPolicy())
        scheduler = registry.resolve(SchedulerProtocol)
    """
    def __init__(self):
        self._bindings: dict = {}
        self._stages: dict = {}   # name -> PipelineStage

    def register(self, protocol: type, implementation) -> None:
        self._bindings[protocol] = implementation

    def resolve(self, protocol: Type[T]) -> T:
        impl = self._bindings.get(protocol)
        if impl is None:
            raise KeyError(
                f"No implementation registered for protocol: {protocol.__name__}"
            )
        return impl

    def registered_protocols(self) -> list:
        return list(self._bindings.keys())

    def register_stage(self, name: str, stage) -> None:
        """Register a PipelineStage by its string name (matches tick_pipeline entries)."""
        self._stages[name] = stage

    def resolve_stage(self, name: str):
        """Resolve a PipelineStage by name. Returns None if not registered."""
        return self._stages.get(name)

    def registered_stages(self) -> list:
        return list(self._stages.keys())
