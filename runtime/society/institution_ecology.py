from runtime.economy.types import AgentId


class InstitutionEcologyModel:
    """
    Manages formation costs, reputation heritage, member cooldown tracking,
    and adaptive knowledge memory decay factors.
    """
    FORMATION_COST_ENERGY = 150
    FORMATION_COST_ATTENTION = 15
    COOLDOWN_TICKS = 15
    BASE_DECAY = 0.01

    def __init__(self):
        # Maps AgentId to tick number until which join actions are in cooldown
        self.member_cooldowns: dict[AgentId, int] = {}

    def get_cooldown_penalty(self, agent_id: AgentId, current_tick: int) -> float:
        """
        Returns penalty to subtract from JoinScore if agent is in split/leave cooldown.
        """
        cooldown_until = self.member_cooldowns.get(agent_id, 0)
        if current_tick < cooldown_until:
            # Shift penalty: higher instability reduces join willingness
            return 2.5
        return 0.0

    def calculate_inherited_reputation(self, founder_reputation: float) -> float:
        """
        Inherits founder prestige: OrgRep = 0.3 * founder_rep + 0.7 * BaseRep (1.0).
        """
        return 0.3 * founder_reputation + 0.7 * 1.0

    def apply_cooldown(self, agent_id: AgentId, current_tick: int) -> None:
        self.member_cooldowns[agent_id] = current_tick + self.COOLDOWN_TICKS

    def calculate_memory_decay(self, citations: int, replications: int) -> float:
        """
        Computes decay scaled by usage/citations.
        Decay = BASE_DECAY / (1.0 + citations * 0.05 + replications * 0.03).
        Clamped between 0.001 and 0.10.
        """
        denom = 1.0 + (citations * 0.05) + (replications * 0.03)
        decay = self.BASE_DECAY / denom
        return max(0.001, min(0.10, decay))


    def calculate_logistic_reputation_gain(self, current_reputation: float, gain: float) -> float:
        """
        Logistic gain prevents prestige inflation: Delta R = gain * (1 - R/5.0).
        """
        delta = gain * (1.0 - (current_reputation / 5.0))
        return min(5.0, current_reputation + delta)

    def apply_prestige_decay(self, current_reputation: float) -> float:
        """
        Gradual prestige decay for inactive organizations.
        """
        decay = 0.005 * (current_reputation / 5.0)
        return max(1.0, current_reputation - decay)

    def evaluate_collapse_score(self, org: OrganizationSnapshot) -> float:
        """
        CollapseScore = 0.35 * B + 0.25 * M + 0.25 * K + 0.15 * R
        B = budget failure (energy < 10)
        M = membership failure (members count == 0)
        K = knowledge integrity failure (1.0 - memory_integrity)
        R = reputation failure (1.0 - reputation/5.0)
        """
        b = 1.0 if org.resources.balances.get("energy", 0) < 10 else 0.0
        m = 1.0 if len(org.members) == 0 else 0.0
        k = 1.0 - org.memory_integrity
        r = 1.0 - (org.reputation / 5.0)

        score = (0.35 * b) + (0.25 * m) + (0.25 * k) + (0.15 * r)
        return score

    def calculate_mutation_pressure(self, environmental_stress: float, stagnation_index: float, resource_pressure: float) -> float:
        """
        Dynamically scales mutation likelihood between 5% and 50% based on environmental stress,
        resource constraints, and theoretical stagnation.
        """
        pressure = 0.05 + (environmental_stress * 0.25) + (stagnation_index * 0.35) + (resource_pressure * 0.20)
        return max(0.05, min(0.50, pressure))

    def calculate_fitness(self, org: OrganizationSnapshot, tick: int) -> float:
        """
        Computes fitness score combining velocity, quality, retention, and innovation potential.
        Scales with log(age) to avoid dinosaur monopolies.
        """
        from runtime.society.organization import OrganizationStage
        if org.stage == OrganizationStage.COLLAPSED:
            return 0.0

        age = max(1, tick - org.created_tick)
        
        # Discovery velocity (completed technologies vs age)
        tech_count = sum(1 for art in org.collective_memory if art.stage.name == "TECHNOLOGY")
        velocity = min(1.0, tech_count / age)

        # Knowledge quality (average confidence of discoveries)
        if org.collective_memory:
            quality = sum(art.confidence for art in org.collective_memory) / len(org.collective_memory)
        else:
            quality = 0.5

        # Member retention rate
        retention = min(1.0, len(org.members) / 10.0) if org.members else 0.0

        # Exploration bias as innovation potential
        potential = org.dna.cognitive_traits[2] if org.dna else 0.5

        # Weighted Fitness
        raw_fitness = (0.4 * velocity) + (0.3 * quality) + (0.2 * retention) + (0.1 * potential)

        import math
        maturity_factor = math.log(age + 1.0)
        
        return raw_fitness * maturity_factor
