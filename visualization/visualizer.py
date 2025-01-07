import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


class Visualizer:
    def __init__(self, grid, obstacles, paths):
        self.grid = grid
        self.obstacles = obstacles
        self.paths = paths

    def save(self, filename):
        """Save the visualization to a file."""
        fig, ax = plt.subplots(figsize=(self.grid.cols / 2, self.grid.rows / 2))  # Scale figure size based on grid size
        
        # Plot obstacles
        for x, y in self.obstacles:
            ax.plot(y, x, "ks", markersize=6)  # Obstacles as black squares with size adjustment
        
        # Plot paths
        for path in self.paths:
            xs, ys = zip(*path["nodes"])
            ax.plot(ys, xs, "-o", markersize=4, linewidth=1.5)  # Paths with smaller markers and thinner lines

        # Set axis limits and labels
        ax.set_xlim(-1, self.grid.cols)
        ax.set_ylim(-1, self.grid.rows)
        ax.set_xticks(range(self.grid.cols))
        ax.set_yticks(range(self.grid.rows))
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
        ax.grid(visible=True, linestyle='--', linewidth=0.5)  # Optional grid for clarity
        
        plt.gca().invert_yaxis()  # Invert y-axis to match grid layout
        plt.savefig(filename)
        plt.close(fig)
