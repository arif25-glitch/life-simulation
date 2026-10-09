
import pygame
from core.engine import MockJevEngine
from core.agent import WoodcutterAgent
from core.world import World
from ui.renderer import Renderer

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jev Life Simulation - Modular")
    clock = pygame.time.Clock()

    world = World()
    agent = WoodcutterAgent("Budi")
    jev = MockJevEngine()
    renderer = Renderer(screen)
    
    current_action = "NONE"
    arrived = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if arrived:
            decision = jev.decide(agent.state, world.state)
            current_action = decision["action"]
            agent.update_state(current_action)
            arrived = False
        
        if agent.move_towards_target():
            arrived = True

        renderer.render_world()
        renderer.render_agent(agent)
        renderer.render_ui(agent, current_action)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
