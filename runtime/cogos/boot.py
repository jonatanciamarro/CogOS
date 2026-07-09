from runtime.cogos.kernel import CogOSKernel
from runtime.core.machine_context import MachineContext
from runtime.memory.graph_engine import GraphKnowledgeEngine

class CogOSBootloader:
    """
    CogOSBootloader handles Power On Self Test (POST), loading invariants,
    and booting the multitasking CogOS Kernel.
    """
    @staticmethod
    def boot():
        # 1. Instantiate the central machine context
        context = MachineContext()
        
        # 2. Mount the Property Graph Database Engine
        graph = GraphKnowledgeEngine()
        
        # 3. Load baseline constitutional nodes (INT000 System Boot)
        graph.add_node("cse://invariant/constitution", "CSE Invariants", "Invariant")
        
        # 4. Instantiate Kernel
        kernel = CogOSKernel(context)
        kernel.system_state.knowledge_graph = graph
        
        # Initialize registries
        graph.update_state_metadata(kernel.system_state.cpu_state)
        
        # 5. Boot Kernel
        kernel.start()
        return kernel
