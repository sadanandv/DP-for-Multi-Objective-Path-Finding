class CostFunctions:
    @staticmethod
    def static_cost(x1, y1, x2, y2):
        # Euclidean distance as the base static cost
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance

    @staticmethod
    def dynamic_cost(x1, y1, x2, y2, time_step, grid, obstacles):
        # Base distance cost
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
        # Time-dependent component (e.g., congestion or time penalty)
        time_penalty = 1 + 0.1 * time_step  # Scale the penalty with time

        # Obstacle proximity penalty
        obstacle_penalty = 0
        for ox, oy in obstacles:
            proximity = max(1, ((ox - x2) ** 2 + (oy - y2) ** 2) ** 0.5)  # Avoid division by zero
            obstacle_penalty += 1 / proximity  # Higher penalty for closer obstacles

        # Total dynamic cost
        #return distance + time_penalty + obstacle_penalty
        return distance
