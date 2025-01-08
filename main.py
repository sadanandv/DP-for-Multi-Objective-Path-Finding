import os
import json
import argparse
import csv
from datetime import datetime
import time

from grid.grid_environment import GridEnvironment
from grid.obstacle_manager import ObstacleManager
from dp_solver.forward_dp import ForwardDP
from dp_solver.backward_dp import BackwardDP
from ranking.rank_paths import RankPaths
from visualization.visualizer import Visualizer
import config

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the Dynamic Programming Pipeline.")
    parser.add_argument("--grid_size", type=str, help="Grid size as ROWS,COLS (e.g., 12,12)")
    parser.add_argument("--connectivity", type=str, help="Connectivity mode: '4-connected' or '8-connected'")
    parser.add_argument("--obstacle_mode", type=str, help="'static' or 'dynamic' obstacle mode")
    parser.add_argument("--obstacle_density", type=float, help="Density of obstacles (e.g., 0.2 for 20%)")
    parser.add_argument("--ranking_criteria", type=str, help="Criteria for ranking paths: 'distance', 'time', etc.")
    parser.add_argument("--sources", type=str, help="Source nodes as a list of tuples (e.g., [(0,0), (1,1)])")
    parser.add_argument("--destinations", type=str, help="Destination nodes as a list of tuples (e.g., [(10,10), (11,11)])")
    args = parser.parse_args()

    # Use config values or command-line arguments
    grid_size = tuple(map(int, args.grid_size.split(','))) if args.grid_size else config.GRID_SIZE
    connectivity = args.connectivity if args.connectivity else config.CONNECTIVITY
    obstacle_mode = args.obstacle_mode if args.obstacle_mode else config.OBSTACLE_MODE
    obstacle_density = args.obstacle_density if args.obstacle_density else config.OBSTACLE_DENSITY
    ranking_criteria = args.ranking_criteria if args.ranking_criteria else config.RANKING_CRITERIA
    sources = eval(args.sources) if args.sources else config.SOURCE_NODES
    destinations = eval(args.destinations) if args.destinations else config.DESTINATION_NODES

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()

    # Initialize grid environment
    grid = GridEnvironment(grid_size, connectivity)

    # Manage obstacles
    obstacle_manager = ObstacleManager(obstacle_mode, obstacle_density)
    obstacles = obstacle_manager.place_obstacles(grid, sources, destinations)
    grid.add_obstacles(obstacles, sources, destinations)

    # Initialize DP solvers
    forward_dp = ForwardDP(grid, sources, destinations)
    backward_dp = BackwardDP(grid, sources, destinations)

    # Solve using DP
    forward_paths = forward_dp.solve()
    backward_paths = backward_dp.solve()

    # Rank paths by cost
    ranker_forward = RankPaths(forward_paths, ranking_criteria)
    ranked_forward_paths = ranker_forward.rank()

    ranker_backward = RankPaths(backward_paths, ranking_criteria)
    ranked_backward_paths = ranker_backward.rank()

    # Calculate execution time
    execution_time = time.time() - start_time

    # Save outputs
    results = {
        "execution_time_seconds": execution_time,
        "ranked_forward_paths": ranked_forward_paths,
        "ranked_backward_paths": ranked_backward_paths,
    }

    with open(os.path.join(output_dir, "results.json"), "w") as json_file:
        json.dump(results, json_file, indent=4)

    with open(os.path.join(output_dir, "results.txt"), "w") as txt_file:
        txt_file.write(f"Execution Time: {execution_time:.2f} seconds\n")
        txt_file.write("Ranked Forward Paths:\n")
        txt_file.writelines(f"{path}\n" for path in ranked_forward_paths)
        txt_file.write("Ranked Backward Paths:\n")
        txt_file.writelines(f"{path}\n" for path in ranked_backward_paths)

    # Visualize ranked paths
    visualizer_forward = Visualizer(grid, obstacles, ranked_forward_paths)
    visualizer_forward.save(os.path.join(output_dir, "forward_paths_visualization.png"), sources, destinations)

    visualizer_backward = Visualizer(grid, obstacles, ranked_backward_paths)
    visualizer_backward.save(os.path.join(output_dir, "backward_paths_visualization.png"), sources, destinations)

    # Prepare CSV output
    csv_file_path = os.path.join("outputs", "experiment_results.csv")
    csv_headers = [
        "timestamp", "grid_size", "connectivity", "obstacle_mode", "obstacle_density",
        "ranking_criteria", "source_node", "destination_node", "complete_path", "path_length",
        "path_cost", "steps_taken", "execution_time", "num_paths"
    ]

    rows = []
    for path in ranked_forward_paths + ranked_backward_paths:
        rows.append([
            timestamp, grid_size, connectivity, obstacle_mode, obstacle_density,
            ranking_criteria, path["nodes"][0], path["nodes"][-1], path["nodes"],
            len(path["nodes"]), path["cost"], path["time"], execution_time,
            len(ranked_forward_paths) + len(ranked_backward_paths)
        ])

    if not os.path.exists(csv_file_path):
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_headers)  # Write headers

    with open(csv_file_path, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)  # Append rows

    print(f"Results saved to {output_dir} and {csv_file_path}")

if __name__ == "__main__":
    main()
