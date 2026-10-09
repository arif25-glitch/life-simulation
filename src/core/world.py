
LOC_COORDS = {
    "HOME": (100, 100),
    "FOREST": (700, 100),
    "MARKET": (400, 500)
}

class World:
    def __init__(self):
        self.state = {"time": "Day", "weather": "Sunny"}
        self.locations = LOC_COORDS
