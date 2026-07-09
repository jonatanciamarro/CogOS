import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runtime.culture.memes import CognitiveMeme
from runtime.culture.tradition import CultureTradition
from runtime.culture.reputation import HistoricalReputation
from runtime.culture.protocol import EmergentProtocol
from runtime.agents.agent import CognitiveAgent

class CB008Runner:
    """
    CB008Runner executes the Cognitive Culture Layer simulation benchmark, evaluating
    Cultural Transmission (CTR), Innovation Velocity (IV), and Consensus Stability (CS).
    """
    @staticmethod
    def run_benchmark():
        print("=== Initializing CogOS Culture Simulator: CB-008 ===")

        # 1. Instantiate culture elements
        protocol = EmergentProtocol()
        reputation = HistoricalReputation()

        # 2. Spawn agents
        parent = CognitiveAgent("ParentTeacher")
        child = CognitiveAgent("ChildApprentice")

        # 3. Register parent strategy traditions
        parent.strategy_memory.add_strategy("tradition_hypothesis_verification")
        parent.strategy_memory.add_strategy("ad_hoc_testing")  # not a tradition

        # 4. Execute inheritance copy
        inherited_count = CultureTradition.inherit_traditions(parent, child)

        # 5. Audit reputation ratios
        parent_id = parent.identity.agent_id
        reputation.record_proposal(parent_id)
        reputation.record_proposal(parent_id)
        reputation.record_commit(parent_id)

        # 6. Replicate Cognitive Meme
        meme = CognitiveMeme("M_formula", "RelativityMeme", parent_id)
        meme.increment_adoption()

        # 7. Convert URI using protocol dictionary
        symbol = protocol.translate_to_symbol("cse://concept/unified_field_theory")
        resolved_uri = protocol.translate_to_uri(symbol)

        # 8. Compute final metrics
        ctr = float(inherited_count)  # 1 tradition copied
        iv = float(meme.adoption_count) # 2 adoptions total
        cs = reputation.get_reputation(parent_id)  # 1/2 commits = 0.50

        print("\n=============================================")
        print("         CB-008 BENCHMARK REPORT             ")
        print("=============================================")
        print(f" Cultural Transmission (CTR):  {ctr:.2f}")
        print(f" Innovation Velocity (IV):    {iv:.2f}")
        print(f" Consensus Stability (CS):     {cs:.2f}")
        print(f" Symbol Translation:           {symbol} -> {resolved_uri}")
        print("=============================================\n")

        return ctr, iv, cs

if __name__ == "__main__":
    CB008Runner.run_benchmark()
