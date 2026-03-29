import os
from .models import CVRPInstance, CVRPSolution
import numpy as np

def parse_vrp_file(file_path: str) -> CVRPInstance:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    name = ""
    dimension = 0
    capacity = 0
    coords = np.zeros((0, 2))
    demands = np.zeros(0)
    depot_id = 0

    section = None
    for line in lines:
        line = line.strip()
        if line.startswith("NAME"):
            name = line.split(":")[1].strip()
        elif line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
            coords = np.zeros((dimension, 2))
            demands = np.zeros(dimension)
        elif line.startswith("CAPACITY"):
            capacity = int(line.split(":")[1].strip())
        elif line.startswith("NODE_COORD_SECTION"):
            section = "coords"
        elif line.startswith("DEMAND_SECTION"):
            section = "demands"
        elif line.startswith("DEPOT_SECTION"):
            section = "depot"
        elif section == "coords" and line:
            parts = line.split()
            node_id = int(parts[0])
            x, y = int(parts[1]), int(parts[2])
            coords[node_id - 1] = x, y
        elif section == "demands" and line:
            parts = line.split()
            node_id = int(parts[0])
            demand = int(parts[1])
            demands[node_id - 1] = demand
        elif section == "depot" and line:
            depot_id = int(line)
            break

    return CVRPInstance(
        name=name,
        dimension=dimension,
        capacity=capacity,
        coords=coords,
        demands=demands,
        depot_id=depot_id
    )

def parse_sol_file(file_path: str) -> CVRPSolution:
    routes = []
    total_distance = 0.0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Route"):
                route = list(map(int, line.split(":")[1].strip().split()))
                routes.append(route)
            elif line.startswith("Cost"):
                total_distance = float(line.split()[1].strip())
    return CVRPSolution(
        algorithm_name='',
        instance_name='',
        routes=routes,
        total_distance=total_distance,
        computation_time=0.0,
        seed=-1
    )