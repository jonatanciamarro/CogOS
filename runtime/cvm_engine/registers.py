class CognitiveRegisters:
    """
    CognitiveRegisters defines helper structures and validation rules for registers CR0-CR8.
    """
    @staticmethod
    def is_valid_register(name):
        return name in [f"CR{i}" for i in range(9)]

    @staticmethod
    def get_register_type(name):
        types = {
            "CR0": "Context",
            "CR1": "Belief",
            "CR2": "EvidenceBuffer",
            "CR3": "Decision",
            "CR4": "Uncertainty",
            "CR5": "ResourceBudget",
            "CR6": "Lineage",
            "CR7": "Attention",
            "CR8": "Purpose"
        }
        return types.get(name, None)
