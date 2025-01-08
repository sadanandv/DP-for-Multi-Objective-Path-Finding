import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
try:
    dynamic_obstacles = pd.read_csv('outputs/[eda]20250108_233137/dynamic_obstacles.csv')
    dynamic_paths = pd.read_csv('outputs/[eda]20250108_233137/dynamic_paths.csv')
    final_ranked_paths = pd.read_csv('outputs/[eda]20250108_233137/final_ranked_paths.csv')
except FileNotFoundError as e:
    print(f"Error loading files: {e}")
    exit()

# Function to summarize datasets
def summarize_data(df, name):
    print(f"\nSummary of {name} Dataset:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(df.describe())
    print(df.info())

# Summarize datasets
summarize_data(dynamic_obstacles, 'Dynamic Obstacles')
summarize_data(dynamic_paths, 'Dynamic Paths')
summarize_data(final_ranked_paths, 'Final Ranked Paths')

# Visualizations
sns.set(style="whitegrid")

# 1. Dynamic Obstacles
if 'time_step' in dynamic_obstacles.columns and 'obstacle_count' in dynamic_obstacles.columns:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=dynamic_obstacles, x='time_step', y='obstacle_count', marker='o')
    plt.title("Dynamic Obstacles Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Obstacle Count")
    plt.show()

# 2. Dynamic Paths Analysis
if 'path_cost' in dynamic_paths.columns and 'time_taken' in dynamic_paths.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=dynamic_paths, x='path_cost', y='time_taken', hue='source_node', style='destination_node')
    plt.title("Path Costs vs Time Taken")
    plt.xlabel("Path Cost")
    plt.ylabel("Time Taken")
    plt.legend(title="Source to Destination")
    plt.show()

# 3. Final Ranked Paths
if 'path_rank' in final_ranked_paths.columns and 'path_cost' in final_ranked_paths.columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=final_ranked_paths, x='path_rank', y='path_cost', palette='viridis')
    plt.title("Path Cost by Rank")
    plt.xlabel("Path Rank")
    plt.ylabel("Path Cost")
    plt.show()

# Correlation heatmap for final ranked paths (numeric columns only)
numeric_cols = final_ranked_paths.select_dtypes(include=['number'])
if numeric_cols.shape[1] > 1:
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix for Final Ranked Paths")
    plt.show()
else:
    print("Not enough numeric columns for correlation matrix.")


# Save insights
try:
    insights = {
        'dynamic_obstacles_summary': dynamic_obstacles.describe().to_dict(),
        'dynamic_paths_summary': dynamic_paths.describe().to_dict(),
        'final_ranked_paths_summary': final_ranked_paths.describe().to_dict()
    }
    with open('eda_insights.json', 'w') as f:
        import json
        json.dump(insights, f, indent=4)
    print("Insights saved to eda_insights.json")
except Exception as e:
    print(f"Error saving insights: {e}")
