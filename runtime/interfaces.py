from typing import Protocol, Any, Dict, List

class ScienceProvider(Protocol):
    """
    Protocol definition for scientific simulation providers.
    """
    def submit_hypothesis(self, concept_uri: str, hypothesis_data: Dict[str, Any]) -> bool:
        ...

    def run_experiment(self, experiment_id: str) -> Dict[str, Any]:
        ...


class HistoryProvider(Protocol):
    """
    Protocol definition for historical archaeology logging providers.
    """
    def log_milestone(self, event_type: str, actor_id: str, details: Dict[str, Any]) -> None:
        ...


class CultureProvider(Protocol):
    """
    Protocol definition for social culture and meme transmission providers.
    """
    def adopt_meme(self, meme_id: str) -> int:
        ...
