# **Dynamic Programming Pipeline for Multi-Objective Pathfinding**

## **Overview**
This project implements a modular pipeline for solving multi-objective pathfinding problems on a 2D grid using **dynamic programming (DP)** principles. Inspired by the paper *"Time Dependency in Multiple Objective Dynamic Programming"* by Michael M. Kostreva and Malgorzata M. Wiecek, the pipeline supports:
- **Static and Dynamic Obstacles**: Obstacles can either remain fixed or move dynamically over time.
- **Multiple Source and Destination Nodes**: Paths are computed between all source and destination node pairs.
- **Path Ranking**: Paths are ranked based on cost metrics (e.g., distance, time) at the end of the experiment.
- **Customizable Execution**: Supports runtime configurations for grid size, connectivity, obstacle properties, and ranking criteria.

---

## **Pipeline Structure**
The project is structured into modular components:

```plaintext
dp_pipeline/
│
├── main.py                      # Entry point to configure and run the pipeline.
├── grid/
│   ├── grid_environment.py      # Handles grid creation and connectivity.
│   ├── obstacle_manager.py      # Manages static or dynamic obstacle behavior.
│   ├── cost_functions.py        # Defines static and dynamic cost functions.
│   └── __init__.py              # Makes the grid folder a package.
│
├── dp_solver/
│   ├── forward_dp.py            # Implements Forward DP for multiple source-destination pairs.
│   ├── backward_dp.py           # Implements Backward DP for multiple source-destination pairs.
│   ├── nondominance.py          # Manages nondominated cost checks.
│   └── __init__.py              # Makes the dp_solver folder a package.
│
├── ranking/
│   ├── rank_paths.py            # Ranks paths based on cost metrics after solving.
│   └── __init__.py              # Makes the ranking folder a package.
│
├── visualization/
│   ├── visualizer.py            # Handles grid, obstacle, and path visualization.
│   └── __init__.py              # Makes the visualization folder a package.
│
├── config.py                    # Global configurations for grid, obstacles, sources, etc.
├── exp_parallel.sh              # Script to run parallel experiments.
├── local_exp.sh                 # Script to run local experiments sequentially.
└── README.md                    # Instructions and details about the pipeline.
```

---

## **Features**
1. **Grid Environment**:
   - Flexible grid sizes with support for 4-connected and 8-connected nodes.
   - Static or dynamic obstacles configurable by the user.
   - Ensures source and destination nodes are obstacle-free.

2. **Dynamic Programming Solvers**:
   - Implements forward and backward DP to find paths between all source and destination nodes.
   - Handles time-dependent costs and nondominance pruning.
   - Tracks and includes time steps (number of moves) in the path evaluation.

3. **Ranking**:
   - Ranks paths based on cost metrics (e.g., shortest distance, minimal time).
   - Supports single and multi-objective ranking criteria, including ranking by time.

4. **Visualization**:
   - Visualizes grid, obstacles, and paths.
   - Highlights source and destination nodes.
   - Animates dynamic obstacle movement if applicable.

5. **Configurable Runtime Options**:
   - Allows specifying grid size, connectivity, obstacle density, and ranking criteria via command-line arguments.
   - Supports custom source and destination nodes.

6. **Parallel and Local Execution**:
   - `exp_parallel.sh`: Runs experiments in parallel, leveraging all available CPU cores.
   - `local_exp.sh`: Runs experiments sequentially for environments without parallel processing support.

---

## **Usage Instructions**

### **1. Create and Activate Virtual Environment**
It is recommended to use a virtual environment to isolate the pipeline dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/MacOS
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

### **2. Configure the Experiment**
You can define the following configurations either in `config.py` or via command-line arguments:
- Grid size and connectivity.
- Sources and destinations (multiple nodes).
- Obstacle mode (static or dynamic).
- Obstacle density and movement patterns (if dynamic).
- Cost function parameters and ranking criteria.

### **3. Run the Pipeline**
To execute the pipeline with default configurations:
```bash
python main.py
```

To override configurations at runtime:
```bash
python main.py \
    --grid_size 12,12 \
    --connectivity 4-connected \
    --obstacle_mode static \
    --obstacle_density 0.4 \
    --ranking_criteria distance \
    --sources "[(0,0),(1,1)]" \
    --destinations "[(10,10),(11,11)]"
```

### **4. Run Experiments in Parallel**
The `exp_parallel.sh` script allows running multiple experiments simultaneously, utilizing all available CPU cores. This is ideal for HPC systems or multi-core environments:
```bash
bash exp_parallel.sh
```

### **5. Run Experiments Sequentially**
The `local_exp.sh` script runs experiments one at a time. This is useful for debugging or environments without parallel processing support:
```bash
bash local_exp.sh
```

### **6. View Results**
- Outputs include:
  - Ranked list of paths with cost metrics.
  - Execution time and number of steps to the destination.
  - Visualizations of the grid and paths.

---

## **Example Configuration**

### **Static Obstacles**
```python
# config.py
GRID_SIZE = (15, 15)
CONNECTIVITY = "8-connected"
OBSTACLE_MODE = "static"
OBSTACLE_DENSITY = 0.2
SOURCE_NODES = [(0, 0), (1, 1)]
DESTINATION_NODES = [(14, 14), (13, 13)]
```

### **Dynamic Obstacles**
```python
# config.py
GRID_SIZE = (15, 15)
CONNECTIVITY = "4-connected"
OBSTACLE_MODE = "dynamic"
OBSTACLE_DENSITY = 0.2
OBSTACLE_MOVEMENT = "random"  # Random or predefined rules
SOURCE_NODES = [(0, 0), (1, 1)]
DESTINATION_NODES = [(14, 14), (13, 13)]
```

---

## **Modules in Detail**

### **1. `grid/`**
- **`grid_environment.py`**: Creates the grid and connectivity structure. Ensures obstacles do not overlap with source or destination nodes.
- **`obstacle_manager.py`**: Places static or dynamic obstacles in the grid.
- **`cost_functions.py`**: Defines static and dynamic costs for node transitions.

### **2. `dp_solver/`**
- **`forward_dp.py`**: Solves forward DP for all source-destination pairs. Includes step count in the results.
- **`backward_dp.py`**: Solves backward DP for all source-destination pairs. Includes step count in the results.
- **`nondominance.py`**: Implements Pareto nondominance checks for cost vectors.

### **3. `ranking/`**
- **`rank_paths.py`**: Ranks paths by cost or time after solving.

### **4. `visualization/`**
- **`visualizer.py`**: Visualizes the grid, obstacles, ranked paths, and highlights source/destination nodes.


---

## **References**
This pipeline is inspired by the paper:
- *"Time Dependency in Multiple Objective Dynamic Programming"*, Michael M. Kostreva and Malgorzata M. Wiecek, Journal of Mathematical Analysis and Applications.
