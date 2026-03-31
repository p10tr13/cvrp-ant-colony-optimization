from .aco_base import ACOBase
from src.models import CVRPInstance
import numpy as np

class MMAS(ACOBase):
    def __init__(self, instance: CVRPInstance, distance_matrix: np.ndarray, parameters):
        super().__init__(instance, distance_matrix, parameters)

        self.tau_max = 1.0
        self.tau_min = 0.001

    def _update_pheromones(self, results):
        if not self.best_result:
            return
        
        iterations_best_route, iterations_best_distance = min(results, key=lambda x: x[1])

        self.tau_max = 1.0 / (self.rho * self.best_result.total_distance)
        self.tau_min = self.tau_max / 20.0

        delta = 1.0 / iterations_best_distance

        for route in iterations_best_route:
            node = self.instance.depot_id - 1

            for next in route:
                self.pheromones[node][next] += delta
                self.pheromones[next][node] += delta
                node = next
            self.pheromones[node][self.instance.depot_id - 1] += delta
            self.pheromones[self.instance.depot_id - 1][node] += delta
        
        self.pheromones = np.clip(self.pheromones, self.tau_min, self.tau_max)

 