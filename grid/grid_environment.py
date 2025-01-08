class GridEnvironment:
    def __init__(self, size, connectivity):
        self.rows, self.cols = size
        self.connectivity = connectivity
        self.grid = [[{"obstacle": False} for _ in range(self.cols)] for _ in range(self.rows)]

    def add_obstacles(self, obstacles, sources, destinations):
        for x, y in obstacles:
            if (x, y) not in sources and (x, y) not in destinations:
                self.grid[x][y]["obstacle"] = True

    def is_obstacle(self, x, y):
        return self.grid[x][y]["obstacle"]

    def neighbors(self, x, y):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # 4-connected
            (-1, -1), (-1, 1), (1, -1), (1, 1) # Diagonals for 8-connected
        ]
        neighbors = []
        for dx, dy in directions[:4] if self.connectivity == "4-connected" else directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and not self.is_obstacle(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
