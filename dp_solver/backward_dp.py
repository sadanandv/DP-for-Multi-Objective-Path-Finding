from queue import PriorityQueue
from grid.cost_functions import CostFunctions

class BackwardDP:
    def __init__(self, grid, sources, destinations):
        self.grid = grid
        self.sources = sources
        self.destinations = destinations

    def solve(self):
        paths = []
        for dest in self.destinations:
            for src in self.sources:
                path = self._solve_from_dest_to_source(dest, src)
                if path:
                    paths.append(path)
        return paths
    
    def _solve_from_dest_to_source(self, source, destination):
        pq = PriorityQueue()
        pq.put((0, [destination], 0))  # (cost, path, steps)
        visited = set()

        while not pq.empty():
            cost, path, steps = pq.get()
            current = path[-1]

            if current in visited:
                continue
            visited.add(current)

            if current == source:
                return {"nodes": path[::-1], "cost": cost, "time": steps}

            for neighbor in self.grid.neighbors(*current):
                if neighbor not in visited:
                    transition_cost = CostFunctions.static_cost(*neighbor, *current)
                    pq.put((cost + transition_cost, path + [neighbor], steps + 1))

        return None  # No path found

