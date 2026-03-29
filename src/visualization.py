import matplotlib.pyplot as plt
import numpy as np
from .models import CVRPInstance, CVRPSolution

def visualize_solution(instance: CVRPInstance, solution: CVRPSolution, title="CVRP Soltion"):
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