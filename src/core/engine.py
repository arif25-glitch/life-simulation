
class MockJevEngine:
    """
    Decision Engine (System 1). 
    Handles the mapping of (AgentState, WorldState) -> Action.
    """
    def decide(self, agent_state, world_state):
        needs = {
            "EAT": agent_state.get("hunger", 0),
            "SLEEP": 100 - agent_state.get("energy", 100),
            "SELL_WOOD": agent_state.get("wood_inventory", 0) * 10,
            "CHOP_TREE": 100 - agent_state.get("wood_inventory", 0)
        }
        best_action = max(needs, key=needs.get)
        
        return {
            "action": best_action,
            "priority": needs[best_action] / 100.0,
            "reasoning_category": "Survival" if best_action in ["EAT", "SLEEP"] else "Economic"
        }
