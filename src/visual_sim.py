import pygame
import json
import random
import time

# --- CONSTANTS ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
COLOR_BG = (30, 30, 30)
COLOR_AGENT = (0, 255, 100)
COLOR_HOME = (100, 100, 250)
COLOR_FOREST = (34, 139, 34)
COLOR_MARKET = (255, 215, 0)
COLOR_TEXT = (255, 255, 255)

# Locations coordinates
LOC_COORDS = {
    "HOME": (100, 100),
    "FOREST": (700, 100),
    "MARKET": (400, 500)
}

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
        self.pos = list(LOC_COORDS["HOME"])
        self.target_pos = list(LOC_COORDS["HOME"])

    def move_towards_target(self):
        # Simple interpolation for movement
        speed = 3
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        dist = (dx**2 + dy**2)**0.5
        
        if dist > speed:
            self.pos[0] += (dx/dist) * speed
            self.pos[1] += (dy/dist) * speed
        else:
            self.pos = list(self.target_pos)
            return True # Arrived
        return False

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jev Life Simulation - Woodcutter")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    agent = WoodcutterAgent("Budi")
    jev = MockJevEngine()
    world_state = {"time": "Day", "weather": "Sunny"}
    
    current_action = "NONE"
    arrived = True

    running = True
    while running:
        screen.fill(COLOR_BG)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Decision Logic
        if arrived:
            decision = jev.decide(agent.state, world_state)
            current_action = decision["action"]
            agent.update_state(current_action)
            arrived = False
        
        # 2. Movement
        if agent.move_towards_target():
            arrived = True

        # 3. Rendering Locations
        pygame.draw.circle(screen, COLOR_HOME, LOC_COORDS["HOME"], 40)
        pygame.draw.circle(screen, COLOR_FOREST, LOC_COORDS["FOREST"], 40)
        pygame.draw.circle(screen, COLOR_MARKET, LOC_COORDS["MARKET"], 40)
        
        screen.blit(font.render("HOME", True, COLOR_TEXT), (LOC_COORDS["HOME"][0]-20, LOC_COORDS["HOME"][1]+50))
        screen.blit(font.render("FOREST", True, COLOR_TEXT), (LOC_COORDS["FOREST"][0]-30, LOC_COORDS["FOREST"][1]+50))
        screen.blit(font.render("MARKET", True, COLOR_TEXT), (LOC_COORDS["MARKET"][0]-30, LOC_COORDS["MARKET"][1]+50))

        # 4. Rendering Agent
        pygame.draw.circle(screen, COLOR_AGENT, (int(agent.pos[0]), int(agent.pos[1])), 15)
        
        # 5. UI Overlay
        stats = [
            f"Agent: {agent.name}",
            f"Action: {current_action}",
            f"Hunger: {agent.state['hunger']}",
            f"Energy: {agent.state['energy']}",
            f"Wood: {agent.state['wood_inventory']}",
            f"Money: {agent.state['money']}"
        ]
        for i, text in enumerate(stats):
            screen.blit(font.render(text, True, COLOR_TEXT), (20, 20 + i*25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
