from queue import PriorityQueue
from grid.cost_functions import CostFunctions


class BackwardDP:
    def __init__(self, grid, sources, destinations):
        self.grid = grid
        self.sources = sources
        self.destinations = destinations

    def solve(self, time_step):
        paths = []
        for dest in self.destinations:
            for src in self.sources:
                partial_path = self._solve_incremental(dest, src, time_step)
                if partial_path:
                    paths.append(partial_path)
        return paths

    def _solve_incremental(self, destination, source, time_step):
        pq = PriorityQueue()
        pq.put((0, [destination], 0))  # (cost, partial_path, steps)
        visited = set()

        while not pq.empty():
            cost, partial_path, steps = pq.get()
            current = partial_path[-1]

            if current in visited or steps > time_step:
                continue
            visited.add(current)

            # If we reach the source or exceed this time step, return the partial path
            if steps == time_step or current == source:
                return {
                    "nodes": partial_path[::-1],  # Reverse the path to match forward order
                    "cost": cost,
                    "time": steps,
                    "completed": current == source,
                }

            for neighbor in self.grid.neighbors(*current):
                if neighbor not in visited:
                    transition_cost = CostFunctions.static_cost(*neighbor, *current)
                    pq.put((cost + transition_cost, partial_path + [neighbor], steps + 1))

        return None  # No valid path found within this time step
    
    def _solve_from_dest_to_source(self, source, destination):
        pq = PriorityQueue()
        pq.put((0, [destination], 0))
        visited = set()
        incomplete_paths = []

        while not pq.empty():
            cost, path, steps = pq.get()
            current = path[-1]

            if current in visited:
                continue
            visited.add(current)

            if current == source:
                return {"nodes": path[::-1], "cost": cost, "time": steps, "completed": True}
            
            obstacle_hit = False
            for neighbor in self.grid.neighbors(*current):
                if neighbor not in visited:
                    transition_cost = CostFunctions.static_cost(*neighbor, *current)
                    pq.put((cost + transition_cost, path + [neighbor], steps + 1))
                elif self.grid.is_obstacle(*neighbor):
                    obstacle_hit = True                

            if obstacle_hit:
                incomplete_paths.append({
                    "nodes": path,
                    "cost": cost,
                    "time": steps,
                    "completed": False
                })

        # Log incomplete paths
        return incomplete_paths
