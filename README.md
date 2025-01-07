
# **Dynamic Programming Pipeline for Multi-Objective Pathfinding**

## **Overview**
This project implements a modular pipeline for solving multi-objective pathfinding problems on a 2D grid using **dynamic programming (DP)** principles. Inspired by the paper *"Time Dependency in Multiple Objective Dynamic Programming"* by Michael M. Kostreva and Malgorzata M. Wiecek, the pipeline supports:
- **Static and Dynamic Obstacles**: Obstacles can either remain fixed or move dynamically over time.
- **Multiple Source and Destination Nodes**: Paths are computed between all source and destination node pairs.
- **Path Ranking**: Paths are ranked based on cost metrics (e.g., distance, time) at the end of the experiment.

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
└── README.md                    # Instructions and details about the pipeline.
```

---

## **Features**
1. **Grid Environment**:
   - Flexible grid sizes with support for 4-connected and 8-connected nodes.
   - Static or dynamic obstacles configurable by the user.

2. **Dynamic Programming Solvers**:
   - Implements forward and backward DP to find paths between all source and destination nodes.
   - Handles time-dependent costs and nondominance pruning.

3. **Ranking**:
   - Ranks paths based on cost metrics (e.g., shortest distance, minimal time).
   - Supports single and multi-objective ranking criteria.

4. **Visualization**:
   - Visualizes grid, obstacles, and paths.
   - Animates dynamic obstacle movement if applicable.

---

## **Usage Instructions**

### **1. Configure the Experiment**
Modify the `config.py` file to define:
- Grid size and connectivity.
- Sources and destinations (multiple nodes).
- Obstacle mode (static or dynamic).
- Obstacle density and movement patterns (if dynamic).
- Cost function parameters and ranking criteria.

### **2. Run the Pipeline**
Use `main.py` to execute the pipeline:
```bash
python main.py
```

### **3. View Results**
- Outputs include:
  - Ranked list of paths with cost metrics.
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
- **`grid_environment.py`**: Creates the grid and connectivity structure.
- **`obstacle_manager.py`**: Places static or dynamic obstacles in the grid.
- **`cost_functions.py`**: Defines static and dynamic costs for node transitions.

### **2. `dp_solver/`**
- **`forward_dp.py`**: Solves forward DP for all source-destination pairs.
- **`backward_dp.py`**: Solves backward DP for all source-destination pairs.
- **`nondominance.py`**: Implements Pareto nondominance checks for cost vectors.

### **3. `ranking/`**
- **`rank_paths.py`**: Ranks paths by cost after solving.

### **4. `visualization/`**
- **`visualizer.py`**: Visualizes the grid, obstacles, and ranked paths.

---

## **Future Enhancements**
- Extend dynamic obstacle behavior to support custom movement rules.
- Add support for more complex cost functions (e.g., energy or environmental factors).
- Enable user-defined grid layouts for non-uniform environments.

---

## **References**
This pipeline is inspired by the paper:
- *"Time Dependency in Multiple Objective Dynamic Programming"*, Michael M. Kostreva and Malgorzata M. Wiecek, Journal of Mathematical Analysis and Applications.

