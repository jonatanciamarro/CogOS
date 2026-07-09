from enum import Enum
from dataclasses import dataclass
from runtime.economy.types import AgentId
from runtime.economy.resource_budget import ResourceBudget
from runtime.science.artifact import KnowledgeArtifact


class OrganizationStage(str, Enum):
    """
    State machine stages of institutional maturity.
    FORMING -> ACTIVE -> EXPANDING -> SPECIALIZED -> RENOWNED -> DECLINING -> DORMANT -> REVIVAL -> COLLAPSED
    """
    FORMING     = "FORMING"
    ACTIVE      = "ACTIVE"
    EXPANDING   = "EXPANDING"
    SPECIALIZED = "SPECIALIZED"
    RENOWNED    = "RENOWNED"
    DECLINING   = "DECLINING"
    DORMANT     = "DORMANT"
    REVIVAL     = "REVIVAL"
    COLLAPSED   = "COLLAPSED"


@dataclass(frozen=True)
class InstitutionDNA:
    """
    Institutional genetic lineage vector.
    Separates cognitive style traits from procedural and cultural values.
    """
    procedural_traits:   tuple[str, ...]             # Research methods, experiment styles
    cognitive_traits:    tuple[float, float, float]  # (abstraction, risk_tolerance, exploration)
    cultural_traits:     tuple[str, ...]             # founding principles, ethics, values
    preferred_niches:    tuple[str, ...] = ("general",)
    mutation_rate:       float = 0.05
    lineage_depth:       int = 0
    parent_org_id:       str | None = None



@dataclass(frozen=True)
class OrganizationSnapshot:
    """
    Immutable snapshot of an institutional group (Laboratories/Universities) at a point in time.
    Supports complete event sourcing reconstruction.
    """
    org_id:             str
    name:               str
    mission:            str
    specialization:     tuple[str, ...]
    stage:              OrganizationStage
    members:            tuple[AgentId, ...]
    reputation:         float
    resources:          ResourceBudget
    collective_memory:  tuple[KnowledgeArtifact, ...]
    created_tick:       int
    research_capacity:  float
    memory_integrity:   float
    dna:                InstitutionDNA | None = None
    dormant_since_tick: int | None = None
    revival_until_tick: int | None = None
    last_active_research_tick: int | None = None

    @property
    def speciation_profile(self) -> str:
        """
        Dynamically classifies the organization type based on its genomic cognitive profile.
        """
        if self.dna is None:
            return "STANDARD_RESEARCH_UNIT"

        # Order of cognitive_traits: (abstraction, risk_tolerance, exploration)
        abstraction, risk, exploration = self.dna.cognitive_traits

        if exploration > 0.7 and risk > 0.6:
            return "INNOVATIVE_EXPLORER"
        elif exploration < 0.3 and risk < 0.3:
            return "CONSERVATIVE_ARCHIVE"
        elif abstraction < 0.4 and exploration > 0.4:
            return "APPLIED_PRACTITIONER"
        elif abstraction > 0.7:
            return "ACADEMIC_THEORIST"
        
        return "STANDARD_RESEARCH_UNIT"


@dataclass(frozen=True)
class SpeciationModifier:
    discovery_speed: float
    memory_retention: float
    energy_cost: float
    innovation_bonus: float


SPECIES_MODIFIERS = {
    "INNOVATIVE_EXPLORER": SpeciationModifier(
        discovery_speed=1.5,
        memory_retention=0.8,
        energy_cost=1.2,
        innovation_bonus=1.5
    ),
    "CONSERVATIVE_ARCHIVE": SpeciationModifier(
        discovery_speed=0.6,
        memory_retention=1.5,
        energy_cost=0.8,
        innovation_bonus=0.5
    ),
    "APPLIED_PRACTITIONER": SpeciationModifier(
        discovery_speed=1.0,
        memory_retention=1.0,
        energy_cost=1.3,
        innovation_bonus=0.8
    ),
    "ACADEMIC_THEORIST": SpeciationModifier(
        discovery_speed=1.2,
        memory_retention=1.1,
        energy_cost=0.9,
        innovation_bonus=1.8
    ),
    "STANDARD_RESEARCH_UNIT": SpeciationModifier(
        discovery_speed=1.0,
        memory_retention=1.0,
        energy_cost=1.0,
        innovation_bonus=1.0
    )
}

