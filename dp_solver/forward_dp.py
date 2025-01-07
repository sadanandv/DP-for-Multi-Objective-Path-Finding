from queue import PriorityQueue
from grid.cost_functions import CostFunctions


class ForwardDP:
    def __init__(self, grid, sources, destinations):
        self.grid = grid
        self.sources = sources
        self.destinations = destinations

    def solve(self):
        paths = []
        for src in self.sources:
            for dest in self.destinations:
                path = self._solve_from_source_to_dest(src, dest)
                if path:
                    paths.append(path)
                    print(f"Path from {src} to {dest}: {path}")
        return paths

    def _solve_from_source_to_dest(self, source, destination):
        # Priority Queue for Dijkstra-like traversal
        pq = PriorityQueue()
        pq.put((0, [source]))  # (cost, path)
        visited = set()

        while not pq.empty():
            cost, path = pq.get()
            current = path[-1]

            if current in visited:
                continue
            visited.add(current)

            # Check if we've reached the destination
            if current == destination:
                return {"nodes": path, "cost": cost}

            # Add neighbors to the queue
            for neighbor in self.grid.neighbors(*current):
                if neighbor not in visited:
                    transition_cost = CostFunctions.static_cost(*current, *neighbor)
                    pq.put((cost + transition_cost, path + [neighbor]))

        return None  # No path found

