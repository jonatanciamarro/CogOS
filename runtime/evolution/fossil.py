from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ExtinctSpeciesRecord:
    org_id: str
    name: str
    profile: str
    birth_tick: float
    death_tick: float
    peak_fitness: float
    artifacts_produced: int


class FossilRecord:
    """
    Keeps track of extinct organizations as fossils for retrospective analysis.
    """
    def __init__(self):
        self.fossils: Dict[str, ExtinctSpeciesRecord] = {}

    def record_fossil(self, record: ExtinctSpeciesRecord) -> None:
        self.fossils[record.org_id] = record

    def get_all_fossils(self) -> List[ExtinctSpeciesRecord]:
        return list(self.fossils.values())
