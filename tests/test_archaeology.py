import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.history.timeline import CognitiveClock
from runtime.history.civilization_memory import CivilizationMemory
from runtime.history.epoch import Epoch
from runtime.history.historical_events import HistoricalEvent

class TestArchaeologySubstrate(unittest.TestCase):
    """
    TestArchaeologySubstrate validates the CognitiveClock ticking bounds, epoch conversions,
    and CivilizationMemory event stream partitions.
    """
    def test_cognitive_clock_ticking(self):
        clock = CognitiveClock(cycles_per_epoch=50, epochs_per_generation=2)
        self.assertEqual(clock.cycle, 0)
        self.assertEqual(clock.epoch, 0)
        self.assertEqual(clock.generation, 0)

        # Tick 50 -> should transition to epoch 1
        clock.tick(50)
        self.assertEqual(clock.cycle, 50)
        self.assertEqual(clock.epoch, 1)
        self.assertEqual(clock.generation, 0)

        # Tick 50 -> should transition to epoch 2 and generation 1 (2 epochs per gen)
        clock.tick(50)
        self.assertEqual(clock.cycle, 100)
        self.assertEqual(clock.epoch, 2)
        self.assertEqual(clock.generation, 1)

    def test_civilization_memory_recording(self):
        clock = CognitiveClock(cycles_per_epoch=10, epochs_per_generation=2)
        memory = CivilizationMemory()

        # Record event in epoch 0
        evt1 = memory.record_civilization_event(clock, "SPAWN", "Agent_1", {"role": "explorer"})
        self.assertEqual(len(memory.event_stream), 1)
        self.assertEqual(evt1.type, "SPAWN")
        self.assertEqual(evt1.epoch, 0)

        # Tick clock to epoch 1
        clock.tick(10)
        evt2 = memory.record_civilization_event(clock, "DISCOVERY", "Agent_1", {"concept": "field_math"})
        self.assertEqual(len(memory.event_stream), 2)
        self.assertEqual(evt2.epoch, 1)

        # Check segmented lists
        self.assertEqual(len(memory.get_epoch(0).events), 1)
        self.assertEqual(len(memory.get_epoch(1).events), 1)

if __name__ == "__main__":
    unittest.main()
