class CivilizationDashboard:
    """
    CivilizationDashboard compiles real-time telemetry reports of the simulated civilization.
    """
    @staticmethod
    def generate_monitor_text(population, cdi, dominant_meme, stage="EARLY SCIENCE"):
        """
        Formats output text for shell displays.
        """
        output = [
            "=============================================",
            "         CogOS Civilization Monitor          ",
            "=============================================",
            f" Active Population:      {population} agents",
            f" Cognitive Diversity:    {cdi:.2f}",
            f" Dominant Meme Node:     {dominant_meme}",
            f" Civilization Stage:     {stage}",
            "============================================="
        ]
        return "\n".join(output)
