class Capability:
    """
    Capability represents a verified execution tool authorization template.
    """
    def __init__(self, name, permission="E-READ", omega_cost=5.0, risk_level=1):
        self.name = name
        self.permission = permission
        self.omega_cost = omega_cost
        self.risk_level = risk_level

    def to_dict(self):
        return {
            "name": self.name,
            "permission": self.permission,
            "omega_cost": self.omega_cost,
            "risk_level": self.risk_level
        }
