import numpy as np
from src.models import CVRPInstance

class Ant:
    def __init__(self, instance: CVRPInstance, distance_matrix: np.ndarray, pheromones: np.ndarray, alpha: float, beta: float, s_max: int, num_vehicles: int):
        self.instance = instance
        self.distance_matrix = distance_matrix
        self.pheromones = pheromones
        self.alpha = alpha
        self.beta = beta
        self.s_max = s_max
        self.num_vehicles = num_vehicles
        self.visited = set()
        self.routes = []
        self.total_distance = 0

    def build_solution(self):
        self.visited = {self.instance.depot_id - 1}
        self.routes = []
        self.total_distance = 0

        for _ in range(self.num_vehicles):
            if len(self.visited) == self.instance.dimension:
                break

            route, distance = self._build_single_route()
            if route:
                self.routes.append(route)
                self.total_distance += distance
        
        if len(self.visited) < self.instance.dimension:
            self.total_distance = float('inf')
        
        return self.routes, self.total_distance
    
    def _build_single_route(self):
        route = []
        current_node = self.instance.depot_id - 1
        current_load = 0
        current_distance = 0

        while True:
            candidates = []
            probabilities = []

            unvisited = [i for i in range(self.instance.dimension) if i not in self.visited]
            for next_node in unvisited:
                distance_to_next = self.distance_matrix[current_node][next_node]
                distance_to_depot = self.distance_matrix[next_node][self.instance.depot_id - 1]

                can_load = current_load + self.instance.demands[next_node] <= self.instance.capacity
                can_come_back = current_distance + distance_to_next + distance_to_depot <= self.s_max

                if can_load and can_come_back:
                    candidates.append(next_node)
                    tau = self.pheromones[current_node][next_node]
                    eta = 1.0 / distance_to_next if distance_to_next > 0 else 0
                    probabilities.append(pow(tau, self.alpha) * pow(eta, self.beta))

            if current_node != self.instance.depot_id - 1 and candidates:
                depot_ind = self.instance.depot_id - 1
                distance_to_depot = self.distance_matrix[current_node][depot_ind]
                candidates.append(depot_ind)
                tau_depot = self.pheromones[current_node][depot_ind]
                eta_depot = 1.0 / distance_to_depot if distance_to_depot > 0 else 0
                probabilities.append(pow(tau_depot, self.alpha) * pow(eta_depot, self.beta))
            
            if not candidates:
                current_distance += self.distance_matrix[current_node][self.instance.depot_id - 1]
                return route, current_distance
            
            probabilities = np.array(probabilities)
            probabilities /= probabilities.sum()

            next_node = np.random.choice(candidates, p=probabilities)

            if next_node == self.instance.depot_id - 1:
                current_distance += self.distance_matrix[current_node][self.instance.depot_id - 1]
                return route, current_distance
            else:
                route.append(next_node)
                self.visited.add(next_node)
                current_load += self.instance.demands[next_node]
                current_distance += self.distance_matrix[current_node][next_node]
                current_node = next_node
