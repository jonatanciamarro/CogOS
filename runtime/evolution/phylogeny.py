from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SpeciesNode:
    org_id: str
    parent_id: Optional[str]
    profile: str
    birth_tick: float
    death_tick: Optional[float] = None
    mutations: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


class PhylogenyTracker:
    """
    Tracks stateful nodes representing institutional lineages.
    Allows navigating evolutionary parent-child relationships and taxonomic mutations.
    """
    def __init__(self):
        self.nodes: Dict[str, SpeciesNode] = {}

    def register_birth(self, org_id: str, parent_id: Optional[str], profile: str, tick: float) -> None:
        """
        Registers the creation of a new institution, updating the parent linkage if applicable.
        """
        node = SpeciesNode(
            org_id=org_id,
            parent_id=parent_id,
            profile=profile,
            birth_tick=tick,
            mutations=[]
        )
        self.nodes[org_id] = node
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children.append(org_id)

    def register_speciation(self, org_id: str, old_profile: str, new_profile: str, tick: float) -> None:
        """
        Logs a taxonomic shift in cognitive DNA style traits.
        """
        if org_id in self.nodes:
            node = self.nodes[org_id]
            node.profile = new_profile
            node.mutations.append(f"speciation:{old_profile}->{new_profile} at tick {tick}")
        else:
            # Fallback birth if node wasn't registered
            self.register_birth(org_id, None, new_profile, tick)

    def register_extinction(self, org_id: str, profile: str, tick: float) -> None:
        """
        Closes the species node lifecycle upon institutional collapse.
        """
        if org_id in self.nodes:
            self.nodes[org_id].death_tick = tick
            self.nodes[org_id].mutations.append(f"extinction at tick {tick}")
