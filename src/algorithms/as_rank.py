import numpy as np
from src.models import CVRPInstance
from .aco_base import ACOBase

class ASRank(ACOBase):
    def __init__(self, instance: CVRPInstance, distance_matrix: np.ndarray, parameters):
        super().__init__(instance, distance_matrix, parameters)
        self.w = parameters.get('w_rank', 6)

    def _update_pheromones(self, results):
        if not results:
            return
        
        sorted_results = sorted(results, key=lambda x: x[1])

        if self.best_result:
            self._add_pheromones_for_solution(self.best_result.routes, self.best_result.total_distance, self.w - 1)
        
        for rank in range(min(len(sorted_results), self.w - 1)):
            routes, distance = sorted_results[rank]
            weight = self.w - (rank + 1)
            if weight > 0:
                self._add_pheromones_for_solution(routes, distance, weight)


    def _add_pheromones_for_solution(self, routes, distance, weight):
        delta = weight / distance

        for route in routes:
            node = self.instance.depot_id - 1

            for next_node in route:
                self.pheromones[node][next_node] += delta
                self.pheromones[next_node][node] += delta
                node = next_node

            self.pheromones[node][self.instance.depot_id - 1] += delta
            self.pheromones[self.instance.depot_id - 1][node] += delta   