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