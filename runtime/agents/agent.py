from runtime.agents.identity import AgentIdentity
from runtime.agents.constitution import AgentConstitution
from runtime.agents.events import AgentEventLog
from runtime.agents.purpose_engine import PurposeEngine
from runtime.agents.agent_state import AgentLifecycleState
from runtime.agents.cognitive_phase import CognitivePhase
from runtime.memory.agent.strategy import StrategyMemory
from runtime.memory.agent.experience import ExperienceMemory
from runtime.memory.agent.failures import FailuresMemory
from runtime.memory.agent.reflection import ReflectionMemory

class CognitiveAgent:
    """
    CognitiveAgent represents an autonomous cognitive entity executing above CVM processes.
    """
    def __init__(self, name, parent_id=None, creation_reason="genesis"):
        self.name = name
        self.identity = AgentIdentity(parent_id, creation_reason)
        self.constitution = AgentConstitution()
        self.event_log = AgentEventLog()
        
        # Initial registers allocation (Purpose Vector CR8)
        self.purpose_vector = {
            "goal": "maximize_knowledge",
            "utility": "accuracy_max",
            "priority": 1.0,
            "constraints": {"uncertainty_limit": 0.3}
        }
        
        self.purpose_engine = PurposeEngine(self)
        self.lifecycle_state = AgentLifecycleState.CREATED
        self.cognitive_phase = CognitivePhase.OBSERVE
        
        self.process_ids = []
        self.capabilities = {}
        
        self.strategy_memory = StrategyMemory()
        self.experience_memory = ExperienceMemory()
        self.failures_memory = FailuresMemory()
        self.reflection_memory = ReflectionMemory()

        # TrustProvider / BudgetProvider contract attributes
        self.trust_score = 0.5
        self.historical_efficiency = 1.0
        self.resource_budget = None   # set by runtime via BudgetPolicy

        # Log genesis creation event
        self.event_log.append("AGENT_CREATED", self.identity.agent_id, {"name": self.name})


    def add_capability(self, capability):
        self.capabilities[capability.name] = capability
        self.event_log.append("CAPABILITY_ADDED", self.identity.agent_id, capability.to_dict())
