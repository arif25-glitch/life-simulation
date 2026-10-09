
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.core.engine import MockJevEngine
from src.core.agent import WoodcutterAgent
from src.core.world import World
import asyncio
import threading

app = FastAPI()

# Global Simulation State
world = World()
agent = WoodcutterAgent("Budi")
jev = MockJevEngine()
current_action = "NONE"
arrived = True

def simulation_loop():
    global current_action, arrived
    while True:
        if arrived:
            decision = jev.decide(agent.state, world.state)
            current_action = decision["action"]
            agent.update_state(current_action)
            arrived = False
        
        if agent.move_towards_target():
            arrived = True
        
        # Tick rate for simulation (approx 60fps)
        import time
        time.sleep(0.016)

# Start simulation in a separate thread
thread = threading.Thread(target=simulation_loop, daemon=True)
thread.start()

@app.get("/state")
async def get_state():
    return {
        "agent": {
            "name": agent.name,
            "pos": agent.pos,
            "state": agent.state
        },
        "action": current_action,
        "locations": world.locations
    }

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("src/web/index.html", "r") as f:
        return f.read()
