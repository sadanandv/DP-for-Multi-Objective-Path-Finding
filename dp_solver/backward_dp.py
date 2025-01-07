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

    def _solve_from_dest_to_source(self, destination, source):
        # Priority Queue for Dijkstra-like traversal
        pq = PriorityQueue()
        pq.put((0, [destination]))  # (cost, path)
        visited = set()

        while not pq.empty():
            cost, path = pq.get()
            current = path[-1]

            if current in visited:
                continue
            visited.add(current)

            # Check if we've reached the source
            if current == source:
                return {"nodes": path[::-1], "cost": cost}  # Reverse path to start from source

            # Add neighbors to the queue (backward traversal)
            for neighbor in self.grid.neighbors(*current):
                if neighbor not in visited:
                    transition_cost = CostFunctions.static_cost(*neighbor, *current)  # Reverse transition cost
                    pq.put((cost + transition_cost, path + [neighbor]))

        return None  # No path found
