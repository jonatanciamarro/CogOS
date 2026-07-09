import math

class CivilizationMetricsEngine:
    """
    CivilizationMetricsEngine tracks diversity indexes, cultural fitness, and collective intelligence levels.
    """
    @staticmethod
    def calculate_cognitive_diversity(agent_strategies):
        """
        CDI = unique_strategies / total_strategies.
        """
        total = len(agent_strategies)
        if total == 0:
            return 1.00
        
        unique = len(set(agent_strategies))
        return unique / total

    @staticmethod
    def calculate_cultural_fitness(adoption, success_rate, longevity_ticks):
        """
        CF = adoption * success_rate * ln(longevity + 1).
        """
        log_factor = math.log(max(1.0, float(longevity_ticks) + 1.0))
        return float(adoption) * float(success_rate) * log_factor

    @staticmethod
    def calculate_innovation_pressure(new_hypotheses_count, accepted_beliefs_count):
        """
        IP = new_hypotheses / accepted_beliefs.
        """
        denom = max(1.0, float(accepted_beliefs_count))
        return float(new_hypotheses_count) / denom
