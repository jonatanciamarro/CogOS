import uuid
from runtime.economy.types import ProposalId, TradeStatus, ResourceType, KnowledgeArtifactType
from runtime.social.trade_proposal import TradeProposal
from runtime.economy.trade_history import TradeHistory
from runtime.bus.event_bus import CogOSEvents, EventPriority


class TradeEngine:
    """
    TradeEngine orchestrates the negotiation process turn-by-turn.
    Ensures that state changes are fully transactional and event-sourced.
    """
    def __init__(self, event_bus=None, history=None):
        self.bus = event_bus
        self.history = history or TradeHistory()

    def propose(self, from_agent_id, to_agent_id, offer, request, tick, parent_id=None, round_num=0) -> TradeProposal:
        """
        Creates an initial TradeProposal and logs it to the history ledger.
        """
        proposal = TradeProposal(
            proposal_id=ProposalId(str(uuid.uuid4())),
            parent_id=parent_id,
            from_agent=from_agent_id,
            to_agent=to_agent_id,
            offer=offer,
            request=request,
            round=round_num,
            expires_tick=tick + 10,
            status=TradeStatus.PROPOSED
        )
        self.history.append("ProposalCreated", proposal, float(tick))
        if self.bus:
            self.bus.publish("ProposalCreated", proposal, EventPriority.NORMAL)
        return proposal

    def evaluate_proposal(self, proposal: TradeProposal, decision_result, tick) -> TradeProposal:
        """
        Processes a DecisionResult on a proposal.
        Transitions the status and appends a new state event.
        Returns a new immutable TradeProposal.
        """
        from runtime.economy.decision_policy import DecisionAction
        action = decision_result.action

        if action == DecisionAction.ACCEPT:
            updated_prop = TradeProposal(
                proposal_id=proposal.proposal_id,
                parent_id=proposal.parent_id,
                from_agent=proposal.from_agent,
                to_agent=proposal.to_agent,
                offer=proposal.offer,
                request=proposal.request,
                round=proposal.round,
                expires_tick=proposal.expires_tick,
                status=TradeStatus.ACCEPTED
            )
            self.history.append("Accepted", updated_prop, float(tick))
            if self.bus:
                self.bus.publish("Accepted", updated_prop, EventPriority.NORMAL)
            return updated_prop

        elif action == DecisionAction.DEFER:
            updated_prop = TradeProposal(
                proposal_id=proposal.proposal_id,
                parent_id=proposal.parent_id,
                from_agent=proposal.from_agent,
                to_agent=proposal.to_agent,
                offer=proposal.offer,
                request=proposal.request,
                round=proposal.round,
                expires_tick=proposal.expires_tick,
                status=TradeStatus.DEFERRED
            )
            self.history.append("ProposalDeferred", updated_prop, float(tick))
            if self.bus:
                self.bus.publish("ProposalDeferred", updated_prop, EventPriority.NORMAL)
            return updated_prop

        elif action == DecisionAction.REJECT:
            updated_prop = TradeProposal(
                proposal_id=proposal.proposal_id,
                parent_id=proposal.parent_id,
                from_agent=proposal.from_agent,
                to_agent=proposal.to_agent,
                offer=proposal.offer,
                request=proposal.request,
                round=proposal.round,
                expires_tick=proposal.expires_tick,
                status=TradeStatus.REJECTED
            )
            self.history.append("Rejected", updated_prop, float(tick))
            if self.bus:
                self.bus.publish("Rejected", updated_prop, EventPriority.NORMAL)
            return updated_prop

        elif action == DecisionAction.COUNTER:
            if proposal.round >= 3:
                # If round limit is reached, reject it
                updated_prop = TradeProposal(
                    proposal_id=proposal.proposal_id,
                    parent_id=proposal.parent_id,
                    from_agent=proposal.from_agent,
                    to_agent=proposal.to_agent,
                    offer=proposal.offer,
                    request=proposal.request,
                    round=proposal.round,
                    expires_tick=proposal.expires_tick,
                    status=TradeStatus.REJECTED
                )
                self.history.append("Rejected", updated_prop, float(tick))
                return updated_prop

            # Create counter-offer: swap offer/request resources
            counter_prop = TradeProposal(
                proposal_id=ProposalId(str(uuid.uuid4())),
                parent_id=proposal.proposal_id,
                from_agent=proposal.to_agent,
                to_agent=proposal.from_agent,
                offer=proposal.request,
                request=proposal.offer,
                round=proposal.round + 1,
                expires_tick=tick + 10,
                status=TradeStatus.COUNTER
            )
            self.history.append("CounterCreated", counter_prop, float(tick))
            if self.bus:
                self.bus.publish("CounterCreated", counter_prop, EventPriority.NORMAL)
            return counter_prop

        return proposal

    def commit_and_execute(self, proposal: TradeProposal, from_agent_obj, to_agent_obj, tick) -> bool:
        """
        Transactional execution cycle:
        1. Validate: Verify resources of both counterparts.
        2. Commit: Log COMMITTED state event.
        3. Execute: Perform resource balances transfer.
        4. Log: Append EXECUTED event to TradeHistory.
        5. Publish: Publish completion event on EventBus.
        """
        if proposal.status != TradeStatus.ACCEPTED:
            return False

        # 1. Validation
        if not self._has_resources(from_agent_obj, proposal.offer):
            return False
        if not self._has_resources(to_agent_obj, proposal.request):
            return False

        # 2. Commit
        committed_prop = TradeProposal(
            proposal_id=proposal.proposal_id,
            parent_id=proposal.parent_id,
            from_agent=proposal.from_agent,
            to_agent=proposal.to_agent,
            offer=proposal.offer,
            request=proposal.request,
            round=proposal.round,
            expires_tick=proposal.expires_tick,
            status=TradeStatus.COMMITTED
        )
        self.history.append("Committed", committed_prop, float(tick))

        # Calculate before utilities for metric tracking
        from runtime.economy.utility_function import WeightedLogUtilityFunction
        from runtime.economy.utility_context import UtilityContext
        
        func_from = getattr(from_agent_obj, "utility_func", None) or WeightedLogUtilityFunction()
        func_to = getattr(to_agent_obj, "utility_func", None) or WeightedLogUtilityFunction()
        
        # Build minimal mock contexts
        mock_env = getattr(getattr(from_agent_obj, "world", None), "environment", None)
        ctx_from = UtilityContext(current_tick=tick, environment=mock_env, counterpart=to_agent_obj)
        ctx_to = UtilityContext(current_tick=tick, environment=mock_env, counterpart=from_agent_obj)

        u_before_a = func_from.evaluate(from_agent_obj, ctx_from)
        u_before_b = func_to.evaluate(to_agent_obj, ctx_to)

        # 3. Execution (Atomic balances updates)
        self._deduct(from_agent_obj, proposal.offer)
        self._add(to_agent_obj, proposal.offer)

        self._deduct(to_agent_obj, proposal.request)
        self._add(from_agent_obj, proposal.request)

        # Calculate after utilities
        u_after_a = func_from.evaluate(from_agent_obj, ctx_from)
        u_after_b = func_to.evaluate(to_agent_obj, ctx_to)

        # 4. Executed event
        executed_prop = TradeProposal(
            proposal_id=proposal.proposal_id,
            parent_id=proposal.parent_id,
            from_agent=proposal.from_agent,
            to_agent=proposal.to_agent,
            offer=proposal.offer,
            request=proposal.request,
            round=proposal.round,
            expires_tick=proposal.expires_tick,
            status=TradeStatus.EXECUTED
        )
        self.history.append("Executed", executed_prop, float(tick))

        # Calculate total resources transferred (sum of numerical amounts)
        res_transferred = sum(item.amount for item in proposal.offer + proposal.request if isinstance(item.resource_type, ResourceType))

        # 5. Event dispatch
        if self.bus:
            from runtime.observability.metric import TradeMetricsEvent
            metrics_evt = TradeMetricsEvent(
                trade_id=proposal.proposal_id,
                utility_before_a=u_before_a,
                utility_after_a=u_after_a,
                utility_before_b=u_before_b,
                utility_after_b=u_after_b,
                resources_transferred=res_transferred,
                negotiation_depth=proposal.round
            )
            self.bus.publish("Executed", executed_prop, EventPriority.NORMAL)
            self.bus.publish("TradeMetricsEvent", metrics_evt, EventPriority.NORMAL)
            self.bus.publish("TRADE_COMPLETED", {"proposal_id": proposal.proposal_id}, EventPriority.NORMAL)

        return True

    def _has_resources(self, agent, items: tuple) -> bool:
        for item in items:
            if isinstance(item.resource_type, ResourceType):
                val = 0.0
                budget = getattr(agent, "resource_budget", None)
                if budget:
                    val = budget.balances.get(item.resource_type.value.lower(), 0.0)
                elif hasattr(agent, "resource_amount"):
                    val = agent.resource_amount(item.resource_type)
                if val < item.amount:
                    return False
        return True

    def _deduct(self, agent, items: tuple):
        for item in items:
            if isinstance(item.resource_type, ResourceType):
                budget = getattr(agent, "resource_budget", None)
                if budget:
                    # ResourceBudget.consume returns BudgetResult
                    budget.consume(item.resource_type.value.lower(), int(item.amount))
                elif hasattr(agent, "deduct_resource"):
                    agent.deduct_resource(item.resource_type, item.amount)

    def _add(self, agent, items: tuple):
        for item in items:
            if isinstance(item.resource_type, ResourceType):
                budget = getattr(agent, "resource_budget", None)
                if budget:
                    budget.replenish(item.resource_type.value.lower(), int(item.amount))
                elif hasattr(agent, "add_resource"):
                    agent.add_resource(item.resource_type, item.amount)
