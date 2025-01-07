import json
from grid.grid_environment import GridEnvironment
from grid.obstacle_manager import ObstacleManager
from dp_solver.forward_dp import ForwardDP
from dp_solver.backward_dp import BackwardDP
from ranking.rank_paths import RankPaths
from visualization.visualizer import Visualizer
import config

def main():
    # Initialize grid environment
    grid = GridEnvironment(config.GRID_SIZE, config.CONNECTIVITY)
    
    # Manage obstacles
    obstacle_manager = ObstacleManager(config.OBSTACLE_MODE, config.OBSTACLE_DENSITY, config.OBSTACLE_MOVEMENT)
    obstacles = obstacle_manager.place_obstacles(grid)

    # Update grid with obstacles
    grid.add_obstacles(obstacles)

    # Initialize DP solvers
    forward_dp = ForwardDP(grid, config.SOURCE_NODES, config.DESTINATION_NODES)
    backward_dp = BackwardDP(grid, config.SOURCE_NODES, config.DESTINATION_NODES)

    # Solve using DP
    forward_paths = forward_dp.solve()
    print("Forward Paths:", forward_paths)

    backward_paths = backward_dp.solve()
    print("Backward Paths:", backward_paths)

    # Rank paths by cost
    ranker_forward = RankPaths(forward_paths, config.RANKING_CRITERIA)
    ranked_forward_paths = ranker_forward.rank()
    print("Ranked Forward Paths:", ranked_forward_paths)

    ranker_backward = RankPaths(backward_paths, config.RANKING_CRITERIA)
    ranked_backward_paths = ranker_backward.rank()
    print("Ranked Backward Paths:", ranked_backward_paths)

    # Save ranked paths to files
    with open("ranked_forward_paths.txt", "w") as f:
        for path in ranked_forward_paths:
            f.write(f"{path}\n")

    with open("ranked_backward_paths.txt", "w") as f:
        for path in ranked_backward_paths:
            f.write(f"{path}\n")

    # Save ranked paths as JSON
    with open("ranked_forward_paths.json", "w") as f:
        json.dump(ranked_forward_paths, f, indent=4)

    with open("ranked_backward_paths.json", "w") as f:
        json.dump(ranked_backward_paths, f, indent=4)

    # Visualize ranked forward paths
    visualizer_forward = Visualizer(grid, obstacles, ranked_forward_paths)
    visualizer_forward.save("forward_paths_visualization.png")

    # Visualize ranked backward paths
    visualizer_backward = Visualizer(grid, obstacles, ranked_backward_paths)
    visualizer_backward.save("backward_paths_visualization.png")

if __name__ == "__main__":
    main()
