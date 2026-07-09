from runtime.agents.agent_state import AgentLifecycleState
from runtime.agents.cognitive_phase import CognitivePhase

class AgentRuntime:
    """
    AgentRuntime manages the execution ticks and cognitive loop state transitions for all active agents.
    """
    def __init__(self, kernel, lifecycle_manager):
        self.kernel = kernel
        self.lifecycle_manager = lifecycle_manager

    def tick_agents(self):
        """
        Advances the cognitive state phase machine of all active agents.
        """
        for agent_id, agent in self.lifecycle_manager.agents.items():
            if agent.lifecycle_state != AgentLifecycleState.ACTIVE:
                continue
                
            self.step_cognitive_loop(agent)

    def step_cognitive_loop(self, agent):
        """
        Cognitive State Machine: Observe -> Interpret -> Hypothesis -> Action -> Result -> Reflect -> Consolidate
        """
        current_phase = agent.cognitive_phase

        if current_phase == CognitivePhase.OBSERVE:
            agent.cognitive_phase = CognitivePhase.INTERPRET
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "INTERPRET"})

        elif current_phase == CognitivePhase.INTERPRET:
            agent.cognitive_phase = CognitivePhase.HYPOTHESIS
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "HYPOTHESIS"})

        elif current_phase == CognitivePhase.HYPOTHESIS:
            agent.cognitive_phase = CognitivePhase.ACTION
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "ACTION"})

        elif current_phase == CognitivePhase.ACTION:
            agent.cognitive_phase = CognitivePhase.RESULT
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "RESULT"})

        elif current_phase == CognitivePhase.RESULT:
            agent.cognitive_phase = CognitivePhase.REFLECT
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "REFLECT"})

        elif current_phase == CognitivePhase.REFLECT:
            # Spawns reflection insights updates
            agent.cognitive_phase = CognitivePhase.CONSOLIDATE
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "CONSOLIDATE"})

        elif current_phase == CognitivePhase.CONSOLIDATE:
            agent.cognitive_phase = CognitivePhase.OBSERVE
            agent.event_log.append("PHASE_TRANSITION", agent.identity.agent_id, {"to": "OBSERVE"})
