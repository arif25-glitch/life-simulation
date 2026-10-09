
from src.core.world import LOC_COORDS

class Agent:
    def __init__(self, name):
        self.name = name
        self.state = {
            "hunger": 20,
            "energy": 100,
            "wood_inventory": 0,
            "money": 0,
            "location": "HOME"
        }
        self.pos = list(LOC_COORDS["HOME"])
        self.target_pos = list(LOC_COORDS["HOME"])

    def move_towards_target(self, speed=3):
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        dist = (dx**2 + dy**2)**0.5
        
        if dist > speed:
            self.pos[0] += (dx/dist) * speed
            self.pos[1] += (dy/dist) * speed
            return False
        else:
            self.pos = list(self.target_pos)
            return True

class WoodcutterAgent(Agent):
    def update_state(self, action):
        if action == "CHOP_TREE":
            self.state["wood_inventory"] += 1
            self.state["energy"] -= 15
            self.state["hunger"] += 10
            self.state["location"] = "FOREST"
            self.target_pos = list(LOC_COORDS["FOREST"])
        elif action == "EAT":
            self.state["hunger"] = max(0, self.state["hunger"] - 40)
            self.state["energy"] += 5
            self.state["location"] = "HOME"
            self.target_pos = list(LOC_COORDS["HOME"])
        elif action == "SLEEP":
            self.state["energy"] = 100
            self.state["hunger"] += 20
            self.state["location"] = "HOME"
            self.target_pos = list(LOC_COORDS["HOME"])
        elif action == "SELL_WOOD":
            earnings = self.state["wood_inventory"] * 10
            self.state["money"] += earnings
            self.state["wood_inventory"] = 0
            self.state["location"] = "MARKET"
            self.target_pos = list(LOC_COORDS["MARKET"])
