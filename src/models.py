from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np

@dataclass
class CVRPInstance:
    name: str
    dimension: int
    capacity: int
    coords: np.ndarray # shape (dimension, 2) for x and y coordinates
    demands: np.ndarray # shape (dimension,) for demand of each node
    depot_id: int = 0

@dataclass
class CVRPSolution:
    algorithm_name: str
    instance_name: str
    routes: List[List[int]] # list of routes, each route is a list of node IDs
    total_distance: float
    computation_time: float
    seed: int
    iteration_history: Optional[List[float]] = field(default=None)