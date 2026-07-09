from runtime.civilization.simulation import Simulation


class SimulationLoop(Simulation):
    """
    SimulationLoop wraps Simulation for backwards compatibility.
    All orchestration runs through the TickPipeline/stages.
    """
    pass
