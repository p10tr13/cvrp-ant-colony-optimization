import math
import numpy as np
from .models import CVRPInstance

def calculate_distance(point1, point2):
    """Calculate the distance between two points in 2D space."""
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def calculate_distance_matrix(instance: CVRPInstance) -> np.ndarray:
    """Calculate the distance matrix for a given CVRP instance."""
    distance_matrix = np.zeros((instance.dimension, instance.dimension))
    nodes = range(instance.dimension)
    for i in nodes:
        for j in nodes:
            if i != j:
                distance_matrix[i][j] = calculate_distance(instance.coords[i], instance.coords[j])
            else:
                distance_matrix[i][j] = 0.0
    return distance_matrix

def calculate_routes_distance(routes, distance_matrix):
    """Calculate the total distance of a given route based on the distance matrix."""
    total_distance = 0.0
    for route in routes:
        full_route = [0] + route + [0]
        for i in range(len(full_route) - 1):
            total_distance += distance_matrix[full_route[i]][full_route[i + 1]]
    return total_distance