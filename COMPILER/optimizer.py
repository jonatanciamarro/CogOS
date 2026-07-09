class CILOptimizer:
    """
    CILOptimizer performs code optimization passes (DKE, semantic instruction fusion).
    """
    @staticmethod
    def optimize(instructions):
        optimized = []
        for line in instructions:
            # Simple optimization: eliminate consecutive identical load operations
            if len(optimized) > 0 and optimized[-1] == line and "LOAD_" in line:
                continue
            optimized.append(line)
        return optimized
