#!/bin/bash

grid_sizes=("8,8" "16,16" "32,32", "64,64", "128,128", "256,256", "512,512", "1024,1024")
connectivities=("4-connected" "8-connected")
obstacle_modes=("static" "dynamic")
obstacle_densities=(0.0 0.2 0.75)
ranks="distance"

OUTPUT_DIR="results_v03_many_to_many"
mkdir -p $OUTPUT_DIR
LOG_FILE="$OUTPUT_DIR/parallel_run_log_v03.txt"
: > $LOG_FILE

MAX_JOBS=$(nproc)
echo "Available cores: $MAX_JOBS"
job_count=0

generate_nodes() {
  local rows=$1
  local cols=$2
  local min_distance=$((rows / 2))

  declare -A selected_nodes
  sources=()
  destinations=()

  is_far_enough() {
    local x1=$1
    local y1=$2
    for node in "${!selected_nodes[@]}"; do
      local x2=${node%,*}
      local y2=${node#*,}
      local dist=$(( (x1 - x2)**2 + (y1 - y2)**2 ))
      if (( dist < min_distance**2 )); then
        return 1  # Not far enough
      fi
    done
    return 0  # Far enough
  }

  for i in $(seq 0 $((rows - 1))); do
    for j in $(seq 0 $((cols - 1))); do
      if is_far_enough $i $j; then
        sources+=("($i,$j)")
        selected_nodes["$i,$j"]=1
      fi
    done
  done

  unset selected_nodes
  declare -A selected_nodes

  for i in $(seq $((rows - 1)) -1 0); do
    for j in $(seq $((cols - 1)) -1 0); do
      if is_far_enough $i $j; then
        destinations+=("($i,$j)")
        selected_nodes["$i,$j"]=1
      fi
    done
  done

  echo "$(IFS=,; echo "[${sources[*]}]")|$(IFS=,; echo "[${destinations[*]}]")"
}


for grid_size in "${grid_sizes[@]}"; do
  IFS="," read -r rows cols <<< "$grid_size"

  for connectivity in "${connectivities[@]}"; do
    for obstacle_mode in "${obstacle_modes[@]}"; do
      for obstacle_density in "${obstacle_densities[@]}"; do

        nodes=$(generate_nodes $rows $cols)
        sources=$(echo "$nodes" | cut -d '|' -f 1)
        destinations=$(echo "$nodes" | cut -d '|' -f 2)

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
