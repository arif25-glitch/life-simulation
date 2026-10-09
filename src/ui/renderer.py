
import pygame
from ..core.world import LOC_COORDS

COLOR_BG = (30, 30, 30)
COLOR_AGENT = (0, 255, 100)
COLOR_HOME = (100, 100, 250)
COLOR_FOREST = (34, 139, 34)
COLOR_MARKET = (255, 215, 0)
COLOR_TEXT = (255, 255, 255)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)

    def render_world(self):
        self.screen.fill(COLOR_BG)
        for loc, coord in LOC_COORDS.items():
            color = COLOR_HOME if loc == "HOME" else COLOR_FOREST if loc == "FOREST" else COLOR_MARKET
            pygame.draw.circle(self.screen, color, coord, 40)
            self.screen.blit(self.font.render(loc, True, COLOR_TEXT), (coord[0]-20, coord[1]+50))

    def render_agent(self, agent):
        pygame.draw.circle(self.screen, COLOR_AGENT, (int(agent.pos[0]), int(agent.pos[1])), 15)

    def render_ui(self, agent, action):
        stats = [
            f"Agent: {agent.name}",
            f"Action: {action}",
            f"Hunger: {agent.state['hunger']}",
            f"Energy: {agent.state['energy']}",
            f"Wood: {agent.state['wood_inventory']}",
            f"Money: {agent.state['money']}"
        ]
        for i, text in enumerate(stats):
            self.screen.blit(self.font.render(text, True, COLOR_TEXT), (20, 20 + i*25))
