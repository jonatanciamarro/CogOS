from runtime.observability.metrics import CivilizationMetricsEngine

class CulturalSelectionEngine:
    """
    CulturalSelectionEngine prunes low-success concept memes based on fitness sweeps.
    """
    def __init__(self, threshold=0.40):
        self.threshold = threshold

    def sweep_meme_node(self, meme, graph_engine, longevity_ticks):
        """
        Evaluates meme fitness; deprecates node confidence if below threshold.
        """
        fitness = CivilizationMetricsEngine.calculate_cultural_fitness(
            meme.adoption_count, 
            meme.confidence, 
            longevity_ticks
        )

        deprecated = False
        if fitness < self.threshold:
            # Prune/deprecate node parameters
            meme.confidence = max(0.10, meme.confidence - 0.20)
            
            node = graph_engine.get_node(meme.id)
            if node:
                node.confidence = max(0.10, node.confidence - 0.20)
            deprecated = True

        return deprecated, fitness
