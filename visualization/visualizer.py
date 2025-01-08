import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('Agg')  # Use non-interactive backend


class Visualizer:
    def __init__(self, grid, obstacles, paths):
        self.grid = grid
        self.obstacles = obstacles
        self.paths = paths

    def save(self, filename, sources, destinations):
        fig, ax = plt.subplots(figsize=(self.grid.cols*1.75, self.grid.rows*1.5))

        for x, y in self.obstacles:
            ax.plot(y, x, "ks", markersize=9, label="_nolegend_")

        for idx, path in enumerate(self.paths):
            xs, ys = zip(*path["nodes"])
            ax.plot(ys, xs, "-o", markersize=8, linewidth=4, label=f"Path {idx + 1}")

        for i, (x, y) in enumerate(sources):
            ax.plot(y, x, "go", markersize=10, label=f"Source {i+1}: ({x}, {y})")
        for i, (x, y) in enumerate(destinations):
            ax.plot(y, x, "ro", markersize=10, label=f"Destination {i+1}: ({x}, {y})")

        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1, 1),
            fontsize="large",
            frameon=True
        )
        ax.set_xlim(-1, self.grid.cols)
        ax.set_ylim(-1, self.grid.rows)
        ax.set_xticks(range(self.grid.cols))
        ax.set_yticks(range(self.grid.rows))
        #ax.set_xlabel("Columns")
        #ax.set_ylabel("Rows")
        ax.grid(visible=True, linestyle='--', linewidth=1.5)

        plt.gca().invert_yaxis()
        plt.savefig(filename)
        plt.close(fig)

    def save_step_visualizations(self, output_dir, step_data):
        for step in step_data:
            fig, ax = plt.subplots(figsize=(self.grid.cols * 1.75, self.grid.rows * 1.5))

            # Plot obstacles for the current step
            for (x, y) in step["positions"]:
                ax.plot(y, x, "ks", markersize=9, label="_nolegend_")  # Obstacles

            # Plot partial paths for the current step
            if "paths" in step and step["paths"]:
                for idx, path in enumerate(step["paths"]):
                    xs, ys = zip(*path["nodes"])
                    ax.plot(ys, xs, "-o", markersize=8, linewidth=4, label=f"Path {idx + 1} (Step {step['time_step']})")

            # Add legend only if there are labeled items
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize="large", frameon=True)
            else:
                print(f"Warning: No paths to plot for time_step {step['time_step']}.")

            ax.set_xlim(-1, self.grid.cols)
            ax.set_ylim(-1, self.grid.rows)
            ax.set_xticks(range(self.grid.cols))
            ax.set_yticks(range(self.grid.rows))
            ax.grid(visible=True, linestyle='--', linewidth=1.5)
            plt.gca().invert_yaxis()  # Match grid layout with (0,0) at top-left
            plt.savefig(os.path.join(output_dir, f"step_{step['time_step']}.png"))
            plt.close(fig)



