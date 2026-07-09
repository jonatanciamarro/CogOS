from runtime.agents.cognitive_phase import CognitivePhase

class CognitiveLoop:
    """
    CognitiveLoop executes rule-based choices during each phase step.
    """
    @staticmethod
    def step_execution(agent, context):
        phase = agent.cognitive_phase
        
        if phase == CognitivePhase.OBSERVE:
            # Reads signals
            agent.event_log.append("LOOP_STEP", agent.identity.agent_id, {"phase": "OBSERVE", "action": "sensing"})
            
        elif phase == CognitivePhase.HYPOTHESIS:
            # Generates belief options
            agent.event_log.append("LOOP_STEP", agent.identity.agent_id, {"phase": "HYPOTHESIS", "action": "conjecturing"})
            
        elif phase == CognitivePhase.REFLECT:
            # Propagates reflections and strategy refinements
            agent.event_log.append("LOOP_STEP", agent.identity.agent_id, {"phase": "REFLECT", "action": "analyzing_failures"})
