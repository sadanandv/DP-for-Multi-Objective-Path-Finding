#!/bin/bash

# Define the parameters for the experiments
grid_sizes=("4,4" "12,12" "64,64" "128,128" "256,256" "512,512" "1024,1024")
connectivities=("4-connected" "8-connected")
obstacle_modes=("static" "dynamic")
obstacle_densities=(0.2 0.4 0.6 0.75)
ranks="distance"

# Scale the source and destination nodes based on grid size
function generate_nodes {
  local grid_size=$1
  local mode=$2
  local num_nodes
  case "$mode" in
    "one-to-one")
      num_nodes=1
      ;;
    "one-to-many")
      num_nodes=$((${grid_size%*x} / 4))
      ;;
    "many-to-one")
      num_nodes=$((${grid_size%*x} / 4))
      ;;
    "many-to-many")
      num_nodes=$((${grid_size%*x} / 2))
      ;;
    *)
      echo "Invalid node mode: $mode"
      exit 1
      ;;
  esac

  echo "$num_nodes"
}

node_modes=("one-to-one" "one-to-many" "many-to-one" "many-to-many")

# Output directory
OUTPUT_DIR="results"
mkdir -p $OUTPUT_DIR

# Log file
LOG_FILE="$OUTPUT_DIR/local_run_log.txt"
: > $LOG_FILE  # Clear the log file

# Iterate through all permutations of configurations
for grid_size in "${grid_sizes[@]}"; do
  for connectivity in "${connectivities[@]}"; do
    for obstacle_mode in "${obstacle_modes[@]}"; do
      for obstacle_density in "${obstacle_densities[@]}"; do
        for node_mode in "${node_modes[@]}"; do

          # Scale source and destination nodes based on the grid size and mode
          num_nodes=$(generate_nodes $grid_size $node_mode)
          sources=$(python3 -c "print([(i, i) for i in range($num_nodes)])")
          destinations=$(python3 -c "print([(i, $num_nodes - i - 1) for i in range($num_nodes)])")

          # Construct the command for this experiment
          command="python3 main.py \
            --grid_size $grid_size \
            --connectivity $connectivity \
            --obstacle_mode $obstacle_mode \
            --obstacle_density $obstacle_density \
            --ranking_criteria $ranks \
            --sources \"$sources\" \
            --destinations \"$destinations\""

          # Execute the experiment
          echo "Running: $command" | tee -a $LOG_FILE
          eval $command >> $LOG_FILE 2>&1

        done
      done
    done
  done
done
