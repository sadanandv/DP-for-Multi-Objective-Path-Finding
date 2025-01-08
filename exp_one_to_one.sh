#!/bin/bash

# Parameters
grid_sizes=("8,8" "16,16" "32,32", "64,64", "128,128", "256,256", "512,512", "1024,1024")
connectivities=("4-connected" "8-connected")
obstacle_modes=("static" "dynamic")
obstacle_densities=(0.0 0.2 0.8)
ranks="distance"

OUTPUT_DIR="results_one_to_one"
mkdir -p $OUTPUT_DIR
LOG_FILE="$OUTPUT_DIR/log_one_to_one.txt"
: > $LOG_FILE  # Clear the log file

MAX_JOBS=$(nproc)
echo "Available cores: $MAX_JOBS"
job_count=0

for grid_size in "${grid_sizes[@]}"; do
  IFS="," read -r rows cols <<< "$grid_size"

  for connectivity in "${connectivities[@]}"; do
    for obstacle_mode in "${obstacle_modes[@]}"; do
      for obstacle_density in "${obstacle_densities[@]}"; do

        sources="[(0,0)]"
        destinations="[($((rows - 1)),$((cols - 1)))]"

        command="python3 main.py \
          --grid_size $grid_size \
          --connectivity $connectivity \
          --obstacle_mode $obstacle_mode \
          --obstacle_density $obstacle_density \
          --ranking_criteria $ranks \
          --sources \"$sources\" \
          --destinations \"$destinations\""

        echo "Running: $command" | tee -a $LOG_FILE
        eval $command >> $LOG_FILE 2>&1 &
        echo "Running Job $job_count."

        ((job_count++))
        if ((job_count >= MAX_JOBS)); then
          wait
          job_count=0
        fi

      done
    done
  done
done

wait

echo "All experiments completed. Results saved to $OUTPUT_DIR."
