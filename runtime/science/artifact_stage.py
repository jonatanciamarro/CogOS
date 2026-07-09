from enum import Enum


class ArtifactStage(str, Enum):
    """
    Categorized stages of maturity for cognitive knowledge artifacts.
    Represents a scientific state machine:
    IDEA -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> THEORY -> TECHNOLOGY
    """
    IDEA       = "IDEA"
    HYPOTHESIS = "HYPOTHESIS"
    EXPERIMENT = "EXPERIMENT"
    EVIDENCE   = "EVIDENCE"
    THEORY     = "THEORY"
    TECHNOLOGY = "TECHNOLOGY"
