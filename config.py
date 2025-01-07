# Configuration for very large grid experiment

# Grid settings
GRID_SIZE = (12, 12)            # Grid dimensions
CONNECTIVITY = "4-connected"      # Connectivity: "4-connected" or "8-connected"

# Obstacle settings
OBSTACLE_MODE = "dynamic"         # "static" or "dynamic"
OBSTACLE_DENSITY = 0.2            # 40% of grid cells as obstacles
OBSTACLE_MOVEMENT = "random"      # Movement type for dynamic obstacles (if any)

# Source and destination nodes
SOURCE_NODES = [(0, 0),(1,11),(10,2)]  # Multiple source nodes
DESTINATION_NODES = [(10,10)]  # Multiple destination nodes

# Ranking criteria
RANKING_CRITERIA = "time"     # Criteria: "distance", "time", etc.