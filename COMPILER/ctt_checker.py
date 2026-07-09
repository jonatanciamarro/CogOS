class CSELCTTChecker:
    """
    CSELCTTChecker validates Cognitive Type Theory (CTT) transitions statically at compile time.
    """
    @staticmethod
    def verify(entities):
        for name, properties in entities.items():
            transformation = properties.get("TRANSFORMATION", "")
            
            # Rejects illegal shortcuts (e.g. Signal directly mapping to Decision)
            if "Signal" in transformation and "Decision" in transformation:
                if "Observation" not in transformation and "Knowledge" not in transformation:
                    raise TypeError(
                        f"CSEL-COMPILE-ERR: Static verification failed in '{name}'. "
                        "Direct transition Signal -> Decision is prohibited by CTT. "
                        "Must transition through intermediate states (Observation -> Belief -> Evidence -> Knowledge)."
                    )
        return True
