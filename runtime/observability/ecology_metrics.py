import statistics
import math
from runtime.observability.metric import Metric, MetricContext
from runtime.society.organization import OrganizationStage


class InstitutionChurnRate:
    """
    ICR = (created + collapsed) / max(1, active * ticks)
    """
    name = "institution_churn_rate"

    def compute(self, context: MetricContext) -> float:
        created = 0
        collapsed = 0

        for event in context.events:
            if hasattr(event, "event_type") or hasattr(event, "__class__"):
                name = getattr(event, "event_type", event.__class__.__name__)
                if "OrganizationCreated" in name:
                    created += 1
                elif "OrganizationCollapsed" in name:
                    collapsed += 1

        snapshots = []
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)

        active = sum(1 for snap in snapshots if snap.stage != OrganizationStage.COLLAPSED)
        ticks = max(1.0, float(context.tick))

        return float(created + collapsed) / max(1.0, float(active) * ticks)


class InstitutionalHalfLife:
    """
    IHL = median ticks until an organization loses 50% of its initial members.
    """
    name = "institutional_half_life"

    def compute(self, context: MetricContext) -> float:
        left_times = []
        for event in context.events:
            if hasattr(event, "event_type") or hasattr(event, "__class__"):
                name = getattr(event, "event_type", event.__class__.__name__)
                if "MemberLeft" in name:
                    left_times.append(getattr(event, "timestamp", 1.0))

        if not left_times:
            return 80.0
        return float(statistics.median(left_times))


class InstitutionalRecoveryTime:
    """
    IRT = Ticks elapsed post-crisis before first new technology is completed.
    """
    name = "institutional_recovery_time"

    def compute(self, context: MetricContext) -> float:
        first_comp = 200.0
        for event in context.events:
            if hasattr(event, "event_type") or hasattr(event, "__class__"):
                name = getattr(event, "event_type", event.__class__.__name__)
                if "ResearchCompleted" in name:
                    ts = getattr(event, "timestamp", 200.0)
                    if ts > 50.0:
                        first_comp = min(first_comp, ts - 50.0)
        return float(first_comp)


class InstitutionDiversityIndex:
    """
    IDI = Shannon Entropy of Speciation Profiles in the active population.
    H = -sum(p_i * ln(p_i))
    """
    name = "institution_diversity_index"

    def compute(self, context: MetricContext) -> float:
        snapshots = []
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)

        active_snaps = [s for s in snapshots if s.stage != OrganizationStage.COLLAPSED]
        if not active_snaps:
            return 0.0

        counts = {}
        for s in active_snaps:
            prof = s.speciation_profile
            counts[prof] = counts.get(prof, 0) + 1

        total = len(active_snaps)
        entropy = 0.0
        for count in counts.values():
            p_i = count / total
            entropy -= p_i * math.log(p_i)
        return float(entropy)


class InstitutionalRecoveryIndex:
    """
    IRI 2.0 = RecoverySpeed * RecoveryDepth * AdaptationFactor * IDI
    """
    name = "institutional_recovery_index"

    def compute(self, context: MetricContext) -> float:
        # 1. Recovery Speed
        irt_calc = InstitutionalRecoveryTime()
        irt = irt_calc.compute(context)
        speed = 1.0 / irt if irt > 0.0 else 0.005

        # 2. Recovery Depth (fraction of surviving organizations)
        survivors = 1
        snapshots = []
        if hasattr(context.world_snapshot, "civilizations"):
            for civ in context.world_snapshot.civilizations:
                for setl in civ.settlements:
                    if hasattr(setl, "institutions"):
                        snapshots.extend(setl.institutions)
        active_snaps = [s for s in snapshots if s.stage != OrganizationStage.COLLAPSED]
        survivors = len(active_snaps)
        depth = min(1.0, (survivors + 1) / 5.0)

        # 3. Shannon Diversity Index (IDI)
        idi_calc = InstitutionDiversityIndex()
        idi = idi_calc.compute(context)

        # 4. Adaptation Rate (fraction of evolved/specialized profiles vs standard)
        specialized = sum(1 for s in active_snaps if s.speciation_profile != "STANDARD_RESEARCH_UNIT")
        adaptation = (specialized / len(active_snaps)) if active_snaps else 0.1

        return float(speed * depth * adaptation * (idi + 0.1))
