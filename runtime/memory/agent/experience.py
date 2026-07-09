class ExperienceMemory:
    """
    ExperienceMemory stores transient observations and past events of the agent.
    """
    def __init__(self):
        self.logs = []

    def add_experience(self, record):
        self.logs.append(record)
