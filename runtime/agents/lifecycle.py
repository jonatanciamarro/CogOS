from runtime.agents.agent import CognitiveAgent
from runtime.agents.agent_state import AgentLifecycleState

class AgentLifecycleManager:
    """
    AgentLifecycleManager handles spawning, suspending, resuming, and archiving Cognitive Agents.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.agents = {}

    def spawn_agent(self, name, parent_agent=None, creation_reason="spawning"):
        """
        Creates a new agent, allocating parent child inheritance profiles.
        """
        parent_id = parent_agent.identity.agent_id if parent_agent else None
        
        # Enforce budget CR5 delegation check if spawned by parent
        if parent_agent:
            parent_budget = parent_agent.purpose_vector["priority"] # Or parent resources
            # Checks if parent has evolve permissions
            if "E-EVOLVE" not in [cap.permission for cap in parent_agent.capabilities.values()]:
                raise PermissionError("E-EVOLVE privilege required to spawn child agents.")
        
        child = CognitiveAgent(name, parent_id, creation_reason)
        child.lifecycle_state = AgentLifecycleState.BOOTING
        
        # Inherit parent constitution
        if parent_agent:
            child.constitution.autonomy_level = parent_agent.constitution.autonomy_level
            child.constitution.risk_tolerance = parent_agent.constitution.risk_tolerance
            child.constitution.evidence_requirement = parent_agent.constitution.evidence_requirement
            
        self.agents[child.identity.agent_id] = child
        child.event_log.append("AGENT_BOOTED", child.identity.agent_id, {})
        return child

    def activate_agent(self, agent_id):
        agent = self.agents.get(agent_id)
        if agent:
            agent.lifecycle_state = AgentLifecycleState.ACTIVE
            agent.event_log.append("AGENT_ACTIVE", agent_id, {})

    def suspend_agent(self, agent_id):
        """
        Suspends the agent, archiving active process thread executions without deleting state.
        """
        agent = self.agents.get(agent_id)
        if agent:
            agent.lifecycle_state = AgentLifecycleState.SUSPENDED
            agent.event_log.append("AGENT_SUSPENDED", agent_id, {})
            
            # Suspend all registered process PIDs
            for pid in agent.process_ids:
                process = self.kernel.system_state.processes.get(pid)
                if process:
                    process.status = "SUSPENDED"

    def resume_agent(self, agent_id):
        """
        Resumes agent, transitioning processes back to scheduler queue.
        """
        agent = self.agents.get(agent_id)
        if agent:
            agent.lifecycle_state = AgentLifecycleState.ACTIVE
            agent.event_log.append("AGENT_RESUMED", agent_id, {})
            
            # Set process PIDs to READY
            for pid in agent.process_ids:
                process = self.kernel.system_state.processes.get(pid)
                if process:
                    process.status = "READY"
