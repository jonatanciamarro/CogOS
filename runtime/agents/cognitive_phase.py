from enum import Enum

class CognitivePhase(Enum):
    """
    CognitivePhase defines the steps of the dynamic loops executed by the agent.
    """
    OBSERVE = 1
    INTERPRET = 2
    HYPOTHESIS = 3
    ACTION = 4
    RESULT = 5
    REFLECT = 6
    CONSOLIDATE = 7
