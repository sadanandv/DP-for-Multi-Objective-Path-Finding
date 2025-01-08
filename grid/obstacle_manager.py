import random

class ObstacleManager:
    def __init__(self, mode, density, movement="random"):
        self.mode = mode
        self.density = density
        self.movement = movement

    def place_obstacles(self, grid, sources, destinations):
        obstacles = []
        if self.mode == "static":
            for _ in range(int(grid.rows * grid.cols * self.density)):
                while True:
                    x, y = random.randint(0, grid.rows - 1), random.randint(0, grid.cols - 1)
                    if not grid.is_obstacle(x, y) and (x, y) not in sources and (x, y) not in destinations:
                        obstacles.append((x, y))
                        break
        elif self.mode == "dynamic":
            for _ in range(int(grid.rows * grid.cols * self.density)):
                x, y = random.randint(0, grid.rows - 1), random.randint(0, grid.cols - 1)
                if (x, y) not in sources and (x, y) not in destinations:
                    obstacles.append((x, y))
        return obstacles

    def update_dynamic_obstacles(self, obstacles, grid):
        new_obstacles = []
        for x, y in obstacles:
            neighbors = grid.neighbors(x, y)
            if neighbors:
                new_obstacles.append(random.choice(neighbors))
            else:
                new_obstacles.append((x, y))
        return new_obstacles
