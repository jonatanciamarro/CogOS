import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.cogos.boot import CogOSBootloader
from runtime.culture.memes import CognitiveMeme
from runtime.culture.selection import CulturalSelectionEngine
from runtime.observability.telemetry import CognitiveTelemetry
from runtime.observability.metrics import CivilizationMetricsEngine
from runtime.observability.dashboard import CivilizationDashboard

class TestObservabilitySubstrate(unittest.TestCase):
    """
    TestObservabilitySubstrate validates bounded circular telemetry buffering,
    selection sweep filters, and CDI diversity metric algorithms.
    """
    def test_telemetry_circular_buffer(self):
        telemetry = CognitiveTelemetry(limit=3)

        telemetry.record_event("A_1", "OBSERVE", "sensing", "success")
        telemetry.record_event("A_1", "ACTION", "search", "success")
        telemetry.record_event("A_1", "REFLECT", "learning", "success")

        self.assertEqual(len(telemetry.buffer), 3)

        # Spawning 4th event pops the 1st
        telemetry.record_event("A_1", "CONSOLIDATE", "commit", "success")
        self.assertEqual(len(telemetry.buffer), 3)
        self.assertEqual(telemetry.buffer[0]["phase"], "ACTION")

    def test_selection_pruning_sweep(self):
        kernel = CogOSBootloader.boot()
        selection = CulturalSelectionEngine(threshold=0.80)

        # Low confidence meme
        meme = CognitiveMeme("cse://invariant/constitution", "Meme_X", "A_1", confidence=0.30)
        meme.adoption_count = 1

        deprecated, fitness = selection.sweep_meme_node(
            meme, 
            kernel.system_state.knowledge_graph, 
            longevity_ticks=2
        )
        self.assertTrue(deprecated)
        self.assertAlmostEqual(meme.confidence, 0.10)  # 0.30 - 0.20

    def test_diversity_metrics_calculator(self):
        cdi_uniform = CivilizationMetricsEngine.calculate_cognitive_diversity(["A", "A", "A"])
        self.assertAlmostEqual(cdi_uniform, 1.0 / 3.0)

        cdi_diverse = CivilizationMetricsEngine.calculate_cognitive_diversity(["A", "B", "C"])
        self.assertAlmostEqual(cdi_diverse, 1.00)

if __name__ == "__main__":
    unittest.main()
