import numpy as np
import time
from src.models import CVRPSolution, CVRPInstance

class GreedyCVRPSolver:
    def __init__(self, instance: CVRPInstance, distance_matrix: np.ndarray, s_max: int, num_vehicles: int) -> None:
        self.instance = instance
        self.distance_matrix = distance_matrix
        self.s_max = s_max
        self.num_vehicles = num_vehicles

    def solve(self) -> CVRPSolution:
        start_time = time.time()

        unvisited = list(range(self.instance.dimension))
        unvisited.remove(self.instance.depot_id - 1)

        routes = []
        total_distance = 0

        for v in range(self.num_vehicles):
            if unvisited.count == 0:
                break

            current_route = []
            current_load = 0
            current_distance = 0
            current_node = self.instance.depot_id - 1

            while unvisited:
                distances = [(node, self.distance_matrix[current_node][node]) for node in unvisited]
                distances.sort(key=lambda x: x[1])

                found_next = False
                for next_node, distance_to_next in distances:
                    distance_to_depot = self.distance_matrix[next_node][self.instance.depot_id - 1]

                    can_load = current_load + self.instance.demands[next_node] <= self.instance.capacity
                    can_come_back = current_distance + distance_to_next + distance_to_depot <= self.s_max

                    if can_load and can_come_back:
                        current_route.append(next_node)
                        current_load += self.instance.demands[next_node]
                        current_distance += distance_to_next
                        current_node = next_node
                        unvisited.remove(next_node)
                        found_next = True
                        break

                if not found_next:
                    current_distance += self.distance_matrix[current_node][self.instance.depot_id - 1]
                    break
            
            if current_route.count != 0:
                routes.append(current_route)
                total_distance += current_distance

        end_time = time.time()

        return CVRPSolution(
            algorithm_name="Greedy (Nearest Neighbours)",
            instance_name=self.instance.name,
            routes=routes,
            total_distance=total_distance,
            computation_time=end_time - start_time,
            seed=-1
        )