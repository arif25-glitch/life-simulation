import json
import random
import time

# --- CONSTANTS ---
ACTIONS = ["CHOP_TREE", "EAT", "SLEEP", "SELL_WOOD"]
LOCATIONS = ["HOME", "FOREST", "MARKET"]

class MockJevEngine:
    def decide(self, agent_state, world_state):
        needs = {
            "EAT": agent_state["hunger"],
            "SLEEP": 100 - agent_state["energy"],
            "SELL_WOOD": agent_state["wood_inventory"] * 10,
            "CHOP_TREE": 100 - agent_state["wood_inventory"]
        }
        best_action = max(needs, key=needs.get)
        action_map = {
            "EAT": "EAT",
            "SLEEP": "SLEEP",
            "SELL_WOOD": "SELL_WOOD",
            "CHOP_TREE": "CHOP_TREE"
        }
        return {
            "action": action_map[best_action],
            "priority": needs[best_action] / 100.0,
            "reasoning_category": "Survival" if best_action in ["EAT", "SLEEP"] else "Economic"
        }

class WoodcutterAgent:
    def __init__(self, name):
        self.name = name
        self.state = {
            "hunger": 20,
            "energy": 100,
            "wood_inventory": 0,
            "money": 0,
            "location": "HOME"
        }

    def update_state(self, action):
        if action == "CHOP_TREE":
            self.state["wood_inventory"] += 1
            self.state["energy"] -= 15
            self.state["hunger"] += 10
            self.state["location"] = "FOREST"
        elif action == "EAT":
            self.state["hunger"] = max(0, self.state["hunger"] - 40)
            self.state["energy"] += 5
            self.state["location"] = "HOME"
        elif action == "SLEEP":
            self.state["energy"] = 100
            self.state["hunger"] += 20
            self.state["location"] = "HOME"
        elif action == "SELL_WOOD":
            earnings = self.state["wood_inventory"] * 10
            self.state["money"] += earnings
            self.state["wood_inventory"] = 0
            self.state["location"] = "MARKET"

    def __str__(self):
        return f"[{self.name}] Loc: {self.state['location']} | Hunger: {self.state['hunger']} | Energy: {self.state['energy']} | Wood: {self.state['wood_inventory']} | Money: {self.state['money']}"

def run_simulation():
    agent = WoodcutterAgent("Budi")
    jev = MockJevEngine()
    world_state = {"time": "Morning", "weather": "Sunny", "trees_available": True}
    
    print(f"Starting Simulation for {agent.name}...")
    print("-" * 50)

    for tick in range(1, 11):
        print(f"Tick {tick}: {agent}")
        decision = jev.decide(agent.state, world_state)
        action = decision["action"]
        print(f"  > Jev Decision: {action} (Priority: {decision['priority']:.2f}, Cat: {decision['reasoning_category']})")
        agent.update_state(action)
        time.sleep(0.1)

    print("-" * 50)
    print("Simulation Finished.")
    print(f"Final State: {agent}")

if __name__ == "__main__":
    run_simulation()
