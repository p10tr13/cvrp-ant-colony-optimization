import matplotlib.pyplot as plt
import numpy as np
from .models import CVRPInstance, CVRPSolution

def visualize_solution(instance: CVRPInstance, solution: CVRPSolution, title="CVRP Solution"):
    plt.figure(figsize=(10,8))
    coords = instance.coords

    cmap = plt.get_cmap('hsv', len(solution.routes) + 1)
    colors = [cmap(i) for i in range(len(solution.routes))]

    for route_idx, route in enumerate(solution.routes):
        full_route = [instance.depot_id - 1] + route + [instance.depot_id - 1]
        route_coords = coords[full_route]

        plt.plot(route_coords[:, 0], route_coords[:, 1], color=colors[route_idx], marker='o', label=f'Vehicle {route_idx + 1}')
    
    plt.scatter(coords[instance.depot_id - 1, 0], coords[instance.depot_id - 1, 1], color='black', marker='s', label='Depot', zorder=5)

    plt.title(f"{title}\nTotal Distance: {solution.total_distance:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def compare_solutions(instance: CVRPInstance, solution1: CVRPSolution, solution2: CVRPSolution):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    for ax, res, title in zip([ax1, ax2], [solution1, solution2], [solution1.algorithm_name, solution2.algorithm_name]):
        coords = instance.coords
        ax.scatter(coords[:, 0], coords[:, 1], color='gray', alpha=0.5, s=20)
        ax.scatter(coords[instance.depot_id - 1, 0], coords[instance.depot_id - 1, 1], 
                   color='black', marker='s', s=80, zorder=5)
        
        colors = plt.get_cmap('hsv')(np.linspace(0, 1, len(res.routes) + 1))
        for i, route in enumerate(res.routes):
            full_route = [instance.depot_id - 1] + route + [instance.depot_id - 1]
            ax.plot(coords[full_route, 0], coords[full_route, 1], color=colors[i], alpha=0.8)
            
        ax.set_title(f"{title} (Dist: {res.total_distance:.2f})")
    
    plt.tight_layout()
    plt.show()
def plot_solutions_side_by_side(instance: CVRPInstance, solutions, title=None, path=None):
    """Draws the routes of several solutions next to each other; saves to `path` or shows the figure."""
    fig, axes = plt.subplots(1, len(solutions), figsize=(6.5 * len(solutions), 5.6), squeeze=False)
    coords = instance.coords
    depot = instance.depot_id - 1

    for ax, solution in zip(axes[0], solutions):
        ax.scatter(coords[:, 0], coords[:, 1], color='gray', s=18, zorder=3)
        colors = plt.get_cmap('tab10')(np.arange(len(solution.routes)) % 10)
        for i, route in enumerate(solution.routes):
            full_route = [depot] + list(route) + [depot]
            ax.plot(coords[full_route, 0], coords[full_route, 1], color=colors[i], lw=1.8, marker='o', ms=4)
        ax.scatter(coords[depot, 0], coords[depot, 1], color='black', marker='s', s=90, zorder=5, label='Depot')
        ax.set_title(f"{solution.algorithm_name}\ntotal distance: {solution.total_distance:.0f}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.legend(loc='lower right')

    if title:
        fig.suptitle(title)
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=110)
        plt.close(fig)
    else:
        plt.show()
