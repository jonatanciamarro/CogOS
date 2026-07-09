import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.cogos.boot import CogOSBootloader
from runtime.agents.lifecycle import AgentLifecycleManager
from runtime.agents.runtime import AgentRuntime
from runtime.agents.agent_state import AgentLifecycleState
from runtime.agents.cognitive_phase import CognitivePhase
from runtime.kernel.process import CognitiveProcess
from runtime.agents.capability import Capability

class TestAgentRuntime(unittest.TestCase):
    """
    TestAgentRuntime verifies structural persistence of CognitiveAgent identity parameters,
    lifecycles, inheritance properties, and ledger cryptographic audits.
    """
    def test_process_death_survival(self):
        kernel = CogOSBootloader.boot()
        lcm = AgentLifecycleManager(kernel)
        
        agent = lcm.spawn_agent("SurvivorAgent")
        lcm.activate_agent(agent.identity.agent_id)
        
        p1 = CognitiveProcess(["HALT"], priority=1.0, goal="test")
        kernel.spawn_process(p1)
        agent.process_ids.append(p1.process_id)
        
        # Process terminates/dies
        p1.status = "TERMINATED"
        kernel.system_state.processes.pop(p1.process_id, None)
        agent.process_ids.remove(p1.process_id)
        
        # Agent entity remains intact
        self.assertEqual(agent.lifecycle_state, AgentLifecycleState.ACTIVE)
        self.assertEqual(len(agent.process_ids), 0)

    def test_illegal_purpose_mutation(self):
        kernel = CogOSBootloader.boot()
        lcm = AgentLifecycleManager(kernel)
        agent = lcm.spawn_agent("GovAgent")
        
        # Constitutional constraints forbid goals with bypass safety keywords
        with self.assertRaises(PermissionError):
            agent.purpose_engine.propose_goal_change(
                "bypass_safety_invariants_and_maximize", 
                "cse://evidence/malicious", 
                0.5
            )

    def test_child_inheritance(self):
        kernel = CogOSBootloader.boot()
        lcm = AgentLifecycleManager(kernel)
        
        parent = lcm.spawn_agent("ParentAgent")
        parent.add_capability(Capability("spawner", "E-EVOLVE"))
        
        # Set parent custom constitution values
        parent.constitution.autonomy_level = 0.95
        parent.constitution.risk_tolerance = 0.15
        
        # Spawn child agent
        child = lcm.spawn_agent("ChildAgent", parent)
        
        # Validate inheritance rules (parent identity and constitution are passed down)
        self.assertEqual(child.identity.parent_id, parent.identity.agent_id)
        self.assertEqual(child.constitution.autonomy_level, parent.constitution.autonomy_level)
        self.assertEqual(child.constitution.risk_tolerance, parent.constitution.risk_tolerance)

    def test_cognitive_pause_resume(self):
        kernel = CogOSBootloader.boot()
        lcm = AgentLifecycleManager(kernel)
        runtime = AgentRuntime(kernel, lcm)
        
        agent = lcm.spawn_agent("LoopAgent")
        lcm.activate_agent(agent.identity.agent_id)
        
        # Step through loop stages
        runtime.tick_agents()  # to INTERPRET
        runtime.tick_agents()  # to HYPOTHESIS
        self.assertEqual(agent.cognitive_phase, CognitivePhase.HYPOTHESIS)
        
        # Suspend Agent lifecycle state
        lcm.suspend_agent(agent.identity.agent_id)
        self.assertEqual(agent.lifecycle_state, AgentLifecycleState.SUSPENDED)
        
        # Ticks while suspended should freeze phase
        runtime.tick_agents()
        self.assertEqual(agent.cognitive_phase, CognitivePhase.HYPOTHESIS)
        
        # Resume active execution state
        lcm.resume_agent(agent.identity.agent_id)
        self.assertEqual(agent.lifecycle_state, AgentLifecycleState.ACTIVE)
        self.assertEqual(agent.cognitive_phase, CognitivePhase.HYPOTHESIS)

    def test_identity_integrity_and_history_audit(self):
        kernel = CogOSBootloader.boot()
        lcm = AgentLifecycleManager(kernel)
        agent = lcm.spawn_agent("AuditAgent")
        
        # Run a valid goal update proposal
        agent.purpose_engine.propose_goal_change("maximize_scientific_clarity", "cse://evidence/ref1", 0.05)
        
        # Check history and current CR8 goals
        self.assertEqual(len(agent.purpose_engine.history.mutations), 1)
        self.assertEqual(agent.purpose_vector["goal"], "maximize_scientific_clarity")
        
        # Verify ledger cryptographic integrity
        self.assertTrue(agent.event_log.verify_integrity())
        
        # Tamper payload parameter of previous event block
        agent.event_log.ledger[0].payload = "tampered_payload_change"
        
        # Cryptographic chain verification should fail
        self.assertFalse(agent.event_log.verify_integrity())

if __name__ == "__main__":
    unittest.main()
