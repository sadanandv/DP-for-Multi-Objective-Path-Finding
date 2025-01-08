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
    parser = argparse.ArgumentParser(description="Run the Dynamic Programming Pipeline.")
    parser.add_argument("--grid_size", type=str, help="Grid size as ROWS,COLS (e.g., 12,12)")
    parser.add_argument("--connectivity", type=str, help="Connectivity mode: '4-connected' or '8-connected'")
    parser.add_argument("--obstacle_mode", type=str, help="'static' or 'dynamic' obstacle mode")
    parser.add_argument("--obstacle_density", type=float, help="Density of obstacles (e.g., 0.2 for 20%)")
    parser.add_argument("--ranking_criteria", type=str, help="Criteria for ranking paths: 'distance', 'time', etc.")
    parser.add_argument("--sources", type=str, help="Source nodes as a list of tuples (e.g., [(0,0), (1,1)])")
    parser.add_argument("--destinations", type=str, help="Destination nodes as a list of tuples (e.g., [(10,10), (11,11)])")
    args = parser.parse_args()

    grid_size = tuple(map(int, args.grid_size.split(','))) if args.grid_size else config.GRID_SIZE
    connectivity = args.connectivity if args.connectivity else config.CONNECTIVITY
    obstacle_mode = args.obstacle_mode if args.obstacle_mode else config.OBSTACLE_MODE
    obstacle_density = args.obstacle_density if args.obstacle_density else config.OBSTACLE_DENSITY
    ranking_criteria = args.ranking_criteria if args.ranking_criteria else config.RANKING_CRITERIA
    sources = eval(args.sources) if args.sources else config.SOURCE_NODES
    destinations = eval(args.destinations) if args.destinations else config.DESTINATION_NODES

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()

    grid = GridEnvironment(grid_size, connectivity)

    obstacle_manager = ObstacleManager(obstacle_mode, obstacle_density)
    obstacles = obstacle_manager.place_obstacles(grid, sources, destinations)
    grid.add_obstacles(obstacles, sources, destinations)

    forward_dp = ForwardDP(grid, sources, destinations)
    backward_dp = BackwardDP(grid, sources, destinations)

    all_paths = []  # Initialize `all_paths` here
    completed_path_ids = set()
    time_step = 0
    all_paths_completed = False
    max_backup_steps = 2048
    stagnation_limit = 50
    no_progress_count = 0

    while not all_paths_completed and time_step < max_backup_steps:
        time_step += 1

        if obstacle_mode == "dynamic":
            obstacle_manager.update_dynamic_obstacles_with_logging(obstacles, grid, time_step)

        forward_paths = forward_dp.solve(time_step)
        backward_paths = backward_dp.solve(time_step)

        new_paths_found = False
        for idx, path in enumerate(forward_paths + backward_paths):
            path_id = path.get("path_id", idx + 1)  # Use existing path_id or assign a unique ID
            if path["completed"] and path_id in completed_path_ids:
                continue
            if path["completed"]:
                completed_path_ids.add(path_id)
            else:
                new_paths_found = True
            all_paths.append({
                "time_step": time_step,
                "path_id": path_id,
                "nodes": path["nodes"],
                "cost": path["cost"],
                "time": path["time"],
                "completed": path["completed"]
            })

        if len(completed_path_ids) == len(destinations):
            all_paths_completed = True

        if not new_paths_found:
            no_progress_count += 1
        else:
            no_progress_count = 0

        if no_progress_count >= stagnation_limit:
            print(f"Warning: No progress for {stagnation_limit} iterations. Stopping.")
            break

    execution_time = time.time() - start_time

    results = {
        "execution_time_seconds": execution_time,
        "completed_paths": sum(1 for path in all_paths if path["completed"]),
    }

    with open(os.path.join(output_dir, "results.json"), "w") as json_file:
        json.dump(results, json_file, indent=4)

    with open(os.path.join(output_dir, "dynamic_paths.csv"), "w", newline="") as path_file:
        path_headers = ["time_step", "path_id", "nodes", "cost", "time", "completed"]
        writer = csv.DictWriter(path_file, fieldnames=path_headers)
        writer.writeheader()
        for path in all_paths:
            writer.writerow({
                "time_step": path["time_step"],
                "path_id": path["path_id"],
                "nodes": path["nodes"],
                "cost": path["cost"],
                "time": path["time"],
                "completed": path["completed"],
            })

    final_paths = [path for path in all_paths if path["completed"]]
    ranked_paths = RankPaths.rank(final_paths, ranking_criteria)

    ranked_path_file = os.path.join(output_dir, "final_ranked_paths.csv")
    rank_headers = ["rank", "path_id", "start_node", "end_node", "nodes", "cost", "time"]
    with open(ranked_path_file, "w", newline="") as rank_file:
        writer = csv.DictWriter(rank_file, fieldnames=rank_headers)
        writer.writeheader()
        for rank, path in enumerate(ranked_paths, start=1):
            writer.writerow({
                "rank": rank,
                "path_id": path["path_id"],
                "start_node": path["nodes"][0],
                "end_node": path["nodes"][-1],
                "nodes": path["nodes"],
                "cost": path["cost"],
                "time": path["time"]
            })

    # Save the final visualization with all completed paths
    visualizer = Visualizer(grid, obstacles, final_paths)
    visualizer.save(os.path.join(output_dir, "final_paths_visualization.png"), sources, destinations)

    print(f"Results saved to {output_dir}")

if __name__ == "__main__":
    main()
