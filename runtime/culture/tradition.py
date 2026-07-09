class CultureTradition:
    """
    CultureTradition copy-propagates parent strategy nodes to child agents.
    """
    @staticmethod
    def inherit_traditions(parent_agent, child_agent):
        """
        Scans parent StrategyMemory logs for items with tradition identifiers and copies them.
        """
        inherited_count = 0
        if hasattr(parent_agent, 'strategy_memory') and parent_agent.strategy_memory:
            for log in parent_agent.strategy_memory.logs:
                if "cultural_tradition" in log.lower() or "tradition_" in log.lower():
                    child_agent.strategy_memory.add_strategy(log)
                    inherited_count += 1
        return inherited_count
