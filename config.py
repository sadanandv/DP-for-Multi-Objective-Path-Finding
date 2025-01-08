# Grid settings
GRID_SIZE = (8, 8)            # Grid dimensions
CONNECTIVITY = "8-connected"      # Connectivity: "4-connected" or "8-connected"

# Obstacle settings
OBSTACLE_MODE = "static"         # "static" or "dynamic"
OBSTACLE_DENSITY = 0.4            # % of grid cells as obstacles
OBSTACLE_MOVEMENT = "random"      # Movement type for dynamic obstacles (if any)

# Source and destination nodes
SOURCE_NODES = [(0, 0)]  # Multiple source nodes
DESTINATION_NODES = [(7,7)]  # Multiple destination nodes

# Ranking criteria
RANKING_CRITERIA = "distance"     # Criteria: "distance", "time"
