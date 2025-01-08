import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


class Visualizer:
    def __init__(self, grid, obstacles, paths):
        self.grid = grid
        self.obstacles = obstacles
        self.paths = paths

    def save(self, filename, sources, destinations):
        fig, ax = plt.subplots(figsize=(self.grid.cols*1.75, self.grid.rows*1.5))

        # Plot obstacles
        for x, y in self.obstacles:
            ax.plot(y, x, "ks", markersize=9, label="_nolegend_")  # Obstacles (black squares)

        # Plot paths
        for idx, path in enumerate(self.paths):
            xs, ys = zip(*path["nodes"])
            ax.plot(ys, xs, "-o", markersize=8, linewidth=4, label=f"Path {idx + 1}")  # Path lines

        # Highlight sources and destinations with unique labels
        for i, (x, y) in enumerate(sources):
            ax.plot(y, x, "go", markersize=10, label=f"Source {i+1}: ({x}, {y})")  # Green for sources
        for i, (x, y) in enumerate(destinations):
            ax.plot(y, x, "ro", markersize=10, label=f"Destination {i+1}: ({x}, {y})")  # Red for destinations

        # Adjust legend
        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1, 1),  # Position legend outside the grid
            fontsize="large",
            frameon=True
        )
        # Set axis limits and labels
        ax.set_xlim(-1, self.grid.cols)
        ax.set_ylim(-1, self.grid.rows)
        ax.set_xticks(range(self.grid.cols))
        ax.set_yticks(range(self.grid.rows))
        #ax.set_xlabel("Columns")
        #ax.set_ylabel("Rows")
        ax.grid(visible=True, linestyle='--', linewidth=1.5)

        plt.gca().invert_yaxis()  # Match grid layout with (0,0) at top-left
        plt.savefig(filename)
        plt.close(fig)


