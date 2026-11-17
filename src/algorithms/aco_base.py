import numpy as np
import time
from .ant import Ant
from src.models import CVRPSolution, CVRPInstance

class ACOBase:
    def __init__(self, instance: CVRPInstance, distance_matrix: np.ndarray, parameters):
        self.instance = instance
        self.distance_matrix = distance_matrix
        self.iterations = parameters.get('iterations', 200)
        self.num_ants = parameters.get('num_ants', 39)
        self.alpha = parameters.get('alpha', 1.0)
        self.beta = parameters.get('beta', 3.0)
        self.rho = parameters.get('rho', 0.5)
        self.s_max = parameters.get('s_max', float('inf'))
        self.num_vehicles = parameters.get('num_vehicles', 5)
        self.record_history = parameters.get('record_history', False)

        self.pheromones = np.full((instance.dimension, instance.dimension), 1.0)
        self.best_result = None

    def solve(self) -> CVRPSolution:
        start = time.time()
        history = []

        for i in range(self.iterations):
            ants = [Ant(self.instance, self.distance_matrix, self.pheromones, self.alpha, self.beta, self.s_max, self.num_vehicles) for _ in range(self.num_ants)]

            results = []
            for ant in ants:
                routes, distance = ant.build_solution()
                if distance < float('inf'):
                    results.append((routes, distance))

                    if self.best_result is None or distance < self.best_result.total_distance:
                        self.best_result = CVRPSolution(
                            algorithm_name=self.__class__.__name__,
                            instance_name=self.instance.name,
                            routes=routes,
                            total_distance=distance,
                            computation_time=0,
                            seed=-1
                        )
            
            self.pheromones *= (1 - self.rho)
            self._update_pheromones(results)

            if self.record_history:
                history.append(self.best_result.total_distance if self.best_result else float('inf'))

            #print(f"Iteration {i}: best solution found: {self.best_result.total_distance if self.best_result else 'None'}")

        if self.best_result:
            self.best_result.computation_time = time.time() - start
            self.best_result.iteration_history = history
            return self.best_result
        # No ant built a feasible solution: report it as infinite distance, not 0
        return CVRPSolution(self.__class__.__name__, self.instance.name, [], float('inf'), time.time() - start, -1, history)

    def _update_pheromones(self, results):
        raise NotImplementedError("Pheromones update should be implemented in algorithm specific subclasses.")
