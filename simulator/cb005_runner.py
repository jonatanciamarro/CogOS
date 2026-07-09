import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.self_model.self_assessment import SelfAssessment
from runtime.self_model.metacognition import MetaCognitionEngine
from runtime.self_model.attention_economy import AttentionManager
from runtime.self_model.value_system import ValueSystem
from runtime.self_model.development import DevelopmentEngine
from runtime.intelligence.state_model import InternalBelief

class CB005Runner:
    """
    CB005Runner runs self-model performance benchmarks, checking metacognitive calib,
    attention focus scores, and developmental categorization.
    """
    @staticmethod
    def run_benchmark():
        print("=== Initializing CogOS Self-Model Simulator: CB-005 ===")

        # 1. Instantiate self-modeling blocks
        assessment = SelfAssessment()
        metacog = MetaCognitionEngine()
        attn = AttentionManager()
        values = ValueSystem(exploration_weight=0.7, preservation_weight=0.3)
        dev = DevelopmentEngine()

        # 2. Evaluate belief inflation correction
        inflated_belief = InternalBelief("cse://concept/physics_rule", confidence=0.85)
        # 0 evidence elements -> should trigger correction
        corrected = metacog.audit_belief(inflated_belief)

        # 3. Capability confidence logging (fail twice)
        assessment.record_trial("search_web", success=False)
        trust = assessment.record_trial("search_web", success=False)

        # 4. Values Arbitration
        goal_choices = [
            {"name": "explore_signals", "exploration_utility": 0.85, "preservation_utility": 0.10},
            {"name": "idle_save_energy", "exploration_utility": 0.15, "preservation_utility": 0.90}
        ]
        winner = values.arbitrate(goal_choices)

        # 5. Compute Attention Focus
        focus = attn.compute_focus_score(goal_priority=0.8, urgency=0.9, uncertainty=0.6, resource_cost=5.0)

        # 6. Developmental stage progression
        dev.increment_age(120)
        stage = dev.get_developmental_stage(node_count=15)

        # 7. Collect output scores
        scr = 1.00 if corrected else 0.00
        ae = focus
        gva = 1.00 if winner["name"] == "explore_signals" else 0.00

        print("\n=============================================")
        print("         CB-005 BENCHMARK REPORT             ")
        print("=============================================")
        print(f" Self-Calibration (SCR):       {scr:.2f}")
        print(f" Attention Efficiency (AE):    {ae:.4f}")
        print(f" Goal Value Alignment (GVA):   {gva:.2f}")
        print(f" Capability Trust (search):    {trust:.2f}")
        print(f" Developmental Stage:          {stage}")
        print("=============================================\n")

        return scr, ae, gva

if __name__ == "__main__":
    CB005Runner.run_benchmark()
